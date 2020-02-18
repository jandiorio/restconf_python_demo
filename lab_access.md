# Programmability Lab Access Details

| hostname | IP address   | SSH  | HTTPS | NETCONF | ASSIGNMENT |
| -------- | ------------ | ---- | ----- | ------- | ---------- |
| CSR1     | 10.246.48.78 | 2271 | 9471  | 871     | Jeff A.    |
| CSR2     | 10.246.48.78 | 2272 | 9472  | 872     | Tafsir T.  |
| CSR3     | 10.246.48.78 | 2273 | 9473  | 873     | Meredith R.|
| CSR4     | 10.246.48.78 | 2274 | 9474  | 874     | Bob L      |
| CSR5     | 10.246.48.78 | 2275 | 9475  | 875     | Tim Hull   |
| CSR6     | 10.246.48.78 | 2276 | 9476  | 876     | Nick T     |
| CSR7     | 10.246.48.78 | 2277 | 9477  | 877     | Joel K     |
| CSR8     | 10.246.48.78 | 2278 | 9478  | 878     | Wade L     |
| CSR9     | 10.246.48.78 | 2279 | 9479  | 879     | Mike P     |
| CSR10    | 10.246.48.78 | 2280 | 9480  | 880     | Brian B    |

## Device Configuration file

```yaml
---
# devices.yml

CSR1:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 871
  device_params:
    name: iosxe

CSR2:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 872
  device_params:
    name: iosxe

CSR3:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 873
  device_params:
    name: iosxe

CSR4:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 874
  device_params:
    name: iosxe

CSR5:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 875
  device_params:
    name: iosxe

CSR6:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 876
  device_params:
    name: iosxe

CSR7:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 877
  device_params:
    name: iosxe

CSR8:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 878
  device_params:
    name: iosxe

CSR9:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 879
  device_params:
    name: iosxe

CSR10:
  host: '10.246.48.78'
  username: 'wwt'
  password: 'WWTwwt1!'
  port: 880
  device_params:
    name: iosxe
```

### Loading device data in Python

```python
with open('devices.yml', 'r') as f:
  devices = yaml.safe_load(f.read())
  csr1 = devices['CSR1']
```
