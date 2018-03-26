# awmepost

This bot do:
 - fetch data from reddit and imgur
 - filter out posts that were already published
 - reformat posts data chunk into list of convenient objects
 - filter posts by tags, scores, etc
 - format and publish posts into separate channels ([imgur and reddit](https://t.me/awmepost),
 - schedule next fetch-filter-publish 
 
Another features:
 - bot provide set of commands to control each channel separately (commands are separated by channel namespaces)
 - commands have convenient style: `/act -s 20` - render graph of activity, `/tags add bad_tag` - ban bad tag, 
 `/subs -h` - print out help message, `/act bla-bla` - show usage msg if command was used wrong, and so on
 - schedule database clean up (remove old posts ids)
 - monitor channels activity and render classy graph of posting frequency (not rly classy actually)