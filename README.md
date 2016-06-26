# chip-gpio
GPIO commands for C.H.I.P. 9$

From the https://getchip.com/pages/chip

# Usage

- Enable GPIO 0

```chip-gpio.py enable 0```

- Disable GPIO 1

```chip-gpio.py disable 1```

- Mode GPIO 2 as output

```chip-gpio.py mode 2 --mode=output```

- Mode GPIO 2 as input

```chip-gpio.py mode 2 --mode=input```

- Write high level on GPIO 0

```chip-gpio.py write 0 --level=high```

- Write low level on GPIO 0

```chip-gpio.py write 0 --level=low```

- Read level on GPIO 1

```chip-gpio.py read 1```


