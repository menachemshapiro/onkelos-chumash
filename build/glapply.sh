# restore gl sources from the Oct 22 backup, apply glfix.tsv, rebuild g/*.json
cd "$(dirname "$0")" && rm -rf gl && cp -r ../bak-oct22/gl gl && python3 glfix.py && python3 gloss_build.py | head -c 80; echo
