rm -rf *.tar.gz
DATE=$(date +"%Y%m%d")
git clone https://github.com/gothfox/Tiny-Tiny-RSS.git Tiny-Tiny-RSS-$DATE
rm Tiny-Tiny-RSS-$DATE/.git -rf
tar cvzf tt-rss-$DATE.tar.gz Tiny-Tiny-RSS-$DATE
rm -rf Tiny-Tiny-RSS-$DATE
#sed work
#version=$(grep -sri 'define version' *.spec | sed 's/%define version //gI')
release=$(grep -sri 'define release' *.spec | sed 's/%define release //gI')
#write to the spec file
sed -i "/%define version/c %define version $DATE" *.spec
sed -i "/changelog/a * $(LC_ALL=C date +"%a %b %d %Y") stephane de Labrusse <stephdl@de-labrusse.fr> $DATE-$release.sme\n- new git version of the day $DATE\n" *.spec
echo ""
echo "Verify in if all is well, then commit the changes"
echo "    git commit -m '* $(LC_ALL=C date +"%a %b %d %Y") stephane de Labrusse <stephdl@de-labrusse.fr> $DATE-$release - new git version of the day $DATE'"
echo ""
