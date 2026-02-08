

```
du -h --max-depth=1 /home | sort -hr | head -n 10
echo "scale=2; $(docker images --format '{{.Size}}' | sed 's/GB/*1024/' | sed 's/MB//' | paste -sd+ - | bc) / 1024" | bc
500GB
```