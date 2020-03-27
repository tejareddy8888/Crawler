@echo off
setlocal enabledelayedexpansion
echo "Started"
set collections =("content" "blog_post" "solution_media_list" "project_action" "watcher" "topic" "tag" "howto_basic" "supply_item" "buildwiki" "files" "user_on_the_web" "category" "post_media" "votes" "challenge_vote_categories" "organization_user" "file_revisions" "discussion" "solution_media" "supply_list" "entry_validation_item" "vote_category" "howto_step" "idea_image_gallery" "howto_step_image" "handbook" "hot_spark" "brainstorm" "featured_news" "malicious_voters" "post_export" "concept_revision" "project_titles" "email_notification_setting" "watched_content" "howto" "challenge_validation_item" "idea" "concept_image_gallery" "notifications" "category_manager" "user" "content_permission" "post" "tagged_item" "activity_digest" "category_set" "entry_revision" "task" "organization" "task_media_list" "challenge_label" "entry_status_history" "featured_content" "challenge" "project_image_gallery" "activity_subscription" "solution" "tag_set" "spotlight" "project" "category_counts" "stream_user" "content_favorite" "activity" "entry" "topic_user" "stream_project" "content_vote")
set ids = ("content_id" "content_id" "activity_id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id" "id")

echo scrapy crawl launchforth_spider -s MONGODB_COLLECTION="content" -s ID_KEY="content_id"
scrapy crawl launchforth_spider -s MONGODB_COLLECTION="content" -s ID_KEY="content_id"