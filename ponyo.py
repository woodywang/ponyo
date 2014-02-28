#!/usr/bin/env python

import os
import sys
import datetime
import util

if __name__ == '__main__':
	context = util.Context.instance()
	util.makeEmptyCommentFile(context.secondMonday)
	pass