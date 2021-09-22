# proxy

0.0.0.0:4000 nginx lb

load test :
k6 run --vus 1000 --iterations 10000 script.js

diagram
![diagram](https://github.com/nicolas-carlini/proxy/blob/main/assets/digram.jpeg)

todo:

- metrics to prometheus
- grafana
- redis cluster
- load test
- try catch in proxy
