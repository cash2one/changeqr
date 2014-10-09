#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Hollay.Yan
# @Date:   2014-10-09 20:54:38
# @Last Modified by:   Hollay.Yan
# @Last Modified time: 2014-10-09 21:23:43

from celery.decorators import task

import logging
import time

logger = logging.getLogger('celery')


@task
def add(x, y):
    logger.info('Sleep 10 second.')
    time.sleep(10)
    logger.info('Wake up.')
    return x + y
