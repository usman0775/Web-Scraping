@echo off
:loop
scrapy crawl find_energy_spider
timeout /t 5 >nul
goto loop