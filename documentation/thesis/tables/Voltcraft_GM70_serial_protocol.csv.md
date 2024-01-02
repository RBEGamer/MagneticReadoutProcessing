: Voltcraft GM70 serial protocol \label{Voltcraft_GM70_serial_protocol.csv}

| BYTE-INDEX | REPRESENTATION |  VALUE                   |
| ---------- | -------------- | ------------------------ |
| 0          | PREAMBLE       | 0x2                      |
| 1          |                | 0x1                      |
| 2          |                | 0x4                      |
| 3          | UNIT           | 'B' => Gauss 'E' => mT   |
| 5          | POLARITY       | '1' => *0.1 '2' => *0.01 |
| 6          | value MSB      | 0x-0xFF                  |
| 13         | value LSB      | 0x-0xFF                  |
| 14         | STOP           | 0x3                      |