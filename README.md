# Python


```python
x = '0301002cc0a8016c00000000797500000000000000000000ffffff00000a000100000028c0a8016c00000000'
x = reduce(lambda x, y: x + struct.pack('B', int(y, 16)),  [a+b for a, b in zip(x[::2], x[1::2])])
print repr(x)
```
