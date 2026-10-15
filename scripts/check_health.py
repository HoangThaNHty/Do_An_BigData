"""Readiness must not claim ready after the resident Spark JVM is lost."""
import unittest
from types import SimpleNamespace
from unittest.mock import Mock
from fastapi import HTTPException
from src.api.main import app,health

class ReadinessChecks(unittest.TestCase):
    def setUp(self):
        self.old_spark=getattr(app.state,'spark',None)
        self.old_market=getattr(app.state,'market',None)
        app.state.market=SimpleNamespace(data={'price':[1,2,3]})
    def tearDown(self):
        app.state.spark=self.old_spark;app.state.market=self.old_market
    def test_live_engine_is_ready(self):
        jsc=Mock();jsc.sc.return_value.isStopped.return_value=False
        app.state.spark=SimpleNamespace(sparkContext=SimpleNamespace(_jsc=jsc))
        self.assertEqual(health()['status'],'ready')
    def test_stopped_engine_is_unavailable(self):
        jsc=Mock();jsc.sc.return_value.isStopped.return_value=True
        app.state.spark=SimpleNamespace(sparkContext=SimpleNamespace(_jsc=jsc))
        with self.assertRaises(HTTPException) as error:health()
        self.assertEqual(error.exception.status_code,503)
    def test_dead_gateway_is_unavailable(self):
        jsc=Mock();jsc.sc.side_effect=ConnectionRefusedError('JVM lost')
        app.state.spark=SimpleNamespace(sparkContext=SimpleNamespace(_jsc=jsc))
        with self.assertRaises(HTTPException) as error:health()
        self.assertEqual(error.exception.status_code,503)
    def test_uninitialized_engine_is_unavailable(self):
        app.state.spark=None
        with self.assertRaises(HTTPException) as error:health()
        self.assertEqual(error.exception.status_code,503)

if __name__=='__main__':unittest.main()
