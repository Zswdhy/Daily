from scrapy import cmdline

name = "richDemo"
cmd = "scrapy crawl %s" % (name)
cmdline.execute(cmd.split())
