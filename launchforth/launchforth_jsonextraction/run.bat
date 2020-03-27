@echo off
setlocal EnableDelayedExpansion

set collections=("content" "content_export" "content_permission" "blog" "category" "tag" "handbook" "file" "challenge" "challenge_validation" "user" "user_on_the_web" "discussion" "topic" "topic_user" "post" "idea" "brainstorm" "entry" "project" )
set ids=("content_id" "content_id" "id" "content_id" "id" "slug" "id" "id" "content_id" "id" "id" "id" "id" "id" "id" "content_id" "content_id" "content_id" "content_id" "content_id")

rem Convert the lists into arrays
set i=0
for %%D in %collections% do (
   set /A i+=1
   set "collections[!i!]=%%D"
)
set i=0
for %%C in %ids% do (
   set /A i+=1
   set "ids[!i!]=%%C"
)

for /L %%A in (1,1,%i%) do (
   ECHO scrapy crawl launchforth -s MONGODB_COLLECTION=!collections[%%A]! -s ID_KEY=!ids[%%A]!
   scrapy crawl launchforth_spider -s MONGODB_COLLECTION=!collections[%%A]! -s ID_KEY=!ids[%%A]!
)