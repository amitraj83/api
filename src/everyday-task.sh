/usr/bin/python3 /root/car-compare/api/src/AutoGenerateComparisons.py
/usr/bin/python3 /root/car-compare/api/src/HTMLGenerator.py
rm -rf /root/car-compare/ui-app/build/blogs/
mv /root/car-compare/ui-app/public/blogs/ /root/car-compare/ui-app/build/
/usr/bin/python3 /root/car-compare/api/src/SiteMapGenerator.py
