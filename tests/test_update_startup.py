"""Background update lifecycle tests, independent of Tk and the network."""
import ast
from pathlib import Path
import threading
import time
import unittest
from unittest.mock import Mock

import editor_runtime as runtime


class Scheduler:
    def __init__(self):
        self.jobs = {}
        self.next_id = 0
        self.owner = threading.get_ident()

    def after(self, milliseconds, callback):
        assert threading.get_ident() == self.owner
        assert milliseconds == 100
        self.next_id += 1
        identifier = str(self.next_id)
        self.jobs[identifier] = callback
        return identifier

    def cancel(self, identifier):
        assert threading.get_ident() == self.owner
        self.jobs.pop(identifier, None)

    def tick(self):
        jobs = list(self.jobs.values())
        self.jobs.clear()
        for callback in jobs:
            callback()

    def until(self, predicate):
        deadline = time.monotonic() + 2
        while not predicate() and time.monotonic() < deadline:
            self.tick()
            time.sleep(0.002)
        assert predicate(), "update worker did not finish"


class UpdateTests(unittest.TestCase):
    def create(self, fetch):
        scheduler = Scheduler()
        results = []

        def receive(result):
            self.assertEqual(threading.get_ident(), scheduler.owner)
            results.append(result)

        controller = runtime.BackgroundUpdateCheck(
            current_version="0.74", fetch=fetch, schedule=scheduler.after,
            cancel=scheduler.cancel, on_result=receive,
        )
        self.addCleanup(controller.close)
        return controller, scheduler, results

    def test_slow_request_does_not_block_ui_or_start_twice(self):
        entered, release = threading.Event(), threading.Event()
        calls = []

        def fetch():
            calls.append(threading.get_ident())
            entered.set()
            release.wait(2)
            return "0.76"

        self.addCleanup(release.set)
        controller, scheduler, results = self.create(fetch)
        controller.start()
        controller.start()
        self.assertTrue(entered.wait(1))
        for _ in range(3):
            scheduler.tick()
        self.assertEqual(results, [])
        self.assertEqual(len(calls), 1)
        self.assertNotEqual(calls[0], threading.get_ident())
        release.set()
        scheduler.until(lambda: bool(results))
        self.assertTrue(results[0].decision.should_open_update_window)
        self.assertEqual(scheduler.jobs, {})

    def test_timeout_returns_error_without_ui_exception(self):
        controller, scheduler, results = self.create(Mock(side_effect=TimeoutError("slow")))
        controller.start()
        scheduler.until(lambda: bool(results))
        self.assertIsNone(results[0].decision)
        self.assertEqual(results[0].error, "slow")

    def test_close_before_start_does_not_fetch(self):
        fetch = Mock()
        controller, scheduler, _ = self.create(fetch)
        controller.close()
        controller.start()
        fetch.assert_not_called()
        self.assertEqual(scheduler.jobs, {})

    def test_close_during_request_cancels_poll_and_ignores_late_result(self):
        entered, release, finished = threading.Event(), threading.Event(), threading.Event()

        def fetch():
            entered.set()
            release.wait(2)
            finished.set()
            return "0.76"

        self.addCleanup(release.set)
        controller, scheduler, results = self.create(fetch)
        controller.start()
        self.assertTrue(entered.wait(1))
        callback = next(iter(scheduler.jobs.values()))
        controller.close()
        controller.close()
        self.assertEqual(scheduler.jobs, {})
        release.set()
        self.assertTrue(finished.wait(1))
        callback()
        self.assertEqual(results, [])
        self.assertEqual(scheduler.jobs, {})

    def test_current_and_blocked_versions_keep_existing_decisions(self):
        for text in ("0.74", runtime.BLOCKED_UPDATE_RESPONSE):
            controller, scheduler, results = self.create(lambda: text)
            controller.start()
            scheduler.until(lambda: bool(results))
            self.assertFalse(results[0].decision.should_open_update_window)
            self.assertEqual(results[0].decision.is_blocked, text == runtime.BLOCKED_UPDATE_RESPONSE)

    def test_editor_fetch_has_timeout_and_checks_http_status(self):
        path = Path(__file__).resolve().parents[1] / "editor.py"
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "fetch_update")
        requests = Mock()
        requests.get.return_value.text = "0.76"
        scope = {"requests": requests, "version_url": "https://example.invalid/version"}
        exec(compile(ast.Module(body=[node], type_ignores=[]), "fetch-update", "exec"), scope)
        self.assertEqual(scope["fetch_update"](), "0.76")
        requests.get.assert_called_once_with(scope["version_url"], timeout=(2, 3))
        requests.get.return_value.raise_for_status.assert_called_once()


if __name__ == "__main__":
    unittest.main()
