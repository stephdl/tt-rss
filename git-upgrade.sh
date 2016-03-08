rm -rf *.tar.gz
DATE=$(date +"%Y%m%d")
git clone https://tt-rss.org/git/tt-rss.git Tiny-Tiny-RSS-$DATE
cd Tiny-Tiny-RSS-$DATE
git log --format=%H | git log --pretty --stdin --no-walk > CHANGELOG.git
COMMIT=$(git log -n 1 --pretty=format:"%h")
cd ../

rm Tiny-Tiny-RSS-$DATE/.git -rf
mv Tiny-Tiny-RSS-$DATE Tiny-Tiny-RSS-$DATE.git$COMMIT
tar cvzf tt-rss-$DATE.git$COMMIT.tar.gz Tiny-Tiny-RSS-$DATE.git$COMMIT

rm -rf Tiny-Tiny-RSS-$DATE.git$COMMIT
#sed work
#version=$(grep -sri 'define version' *.spec | sed 's/%define version //gI')
release=$(grep -sri 'define release' *.spec | sed 's/%define release //gI')
#write to the spec file
sed -i "/%define version/c %define version $DATE.git$COMMIT" *.spec
sed -i "/changelog/a * $(LC_ALL=C date +"%a %b %d %Y") stephane de Labrusse <stephdl@de-labrusse.fr> $DATE.git$COMMIT-$release\n- new git version of the day $DATE\n" *.spec
echo ""
echo " Verify if all is well, then commit the changes"
echo " git add . -A ; git commit -m '* $(LC_ALL=C date +"%a %b %d %Y") stephane de Labrusse <stephdl@de-labrusse.fr> $DATE.git$COMMIT-$release - new git version of the day $DATE'"
echo " git push --tags origin branchname"

