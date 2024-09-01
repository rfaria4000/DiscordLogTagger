import pytest
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def inc(x: int) -> int:
  return x + 1

def test_inc():
  assert inc(2) == 3
  assert inc(4) == 5