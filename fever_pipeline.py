#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time

import websocket


__author__ = ['chaonan99']


class FEVERPredict(object):
  """docstring for FEVERPredict"""
  ws_path = "ws://bvisionserver4.cs.unc.edu:9027/demo"
  def __init__(self):
    super(FEVERPredict, self).__init__()

  def _predict(self, claim_text):
    ws_obj = websocket.create_connection(self.ws_path)

    message = json.dumps(claim_text)
    ws_obj.send(message)
    result = json.loads(ws_obj.recv())
    return result

    ## yijin TODO
    # return {'predicted_evidence': ['test message'],
    #         'docids': ['University_of_North_Carolina_at_Chapel_Hill'],
    #         'predicted_label': 'SUPPORTS'}

  def predict(self, claim_text):
    results = self._predict(claim_text)
    # time.sleep(5)
    return {'predicted_evidence': '@_@'.join(results['predicted_evidence']),
            'docids': '@_@'.join(results['docids']),
            'predicted_label': results['predicted_label']}


def main():
  pass


if __name__ == '__main__':
  main()