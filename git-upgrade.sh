rm -rf *.tar.gz
git clone https://github.com/gothfox/Tiny-Tiny-RSS.git Tiny-Tiny-RSS-$(date +"%Y%m%d")
rm Tiny-Tiny-RSS-$(date +"%Y%m%d")/.git -rf
tar cvzf tt-rss-$(date +"%Y%m%d").tar.gz Tiny-Tiny-RSS-$(date +"%Y%m%d")
rm -rf Tiny-Tiny-RSS-$(date +"%Y%m%d")
