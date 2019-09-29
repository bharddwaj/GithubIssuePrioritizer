SELECT
  REGEXP_REPLACE(title, r"\s{2,}", ',') AS issue_title,
  REGEXP_REPLACE(body, r"\s{2,}", ',') AS body,
  ARRAY_TO_STRING(names, ",") labels,
  DATE_DIFF(time_closed, time_created, DAY) n_days_open
FROM (
  SELECT
    LOWER(TRIM(REGEXP_REPLACE(JSON_EXTRACT(payload,
            '$.issue.title'), r"\\n|\(|\)|\[|\]|#|\*|`|\"", ' '))) AS title,
    LOWER(TRIM(REGEXP_REPLACE(JSON_EXTRACT(payload,
            '$.issue.body'), r"\\n|\(|\)|\[|\]|#|\*|`|\"", ' '))) AS body,
            CAST( REGEXP_REPLACE(SPLIT(LOWER(JSON_EXTRACT(payload,
            '$.issue.created_at')), 't')[OFFSET(0)], r"[^-0-9]", "")  as DATE) AS time_created,
             CAST(REGEXP_REPLACE(SPLIT(LOWER(JSON_EXTRACT(payload,
            '$.issue.closed_at')), "t")[OFFSET(0)], r"[^-0-9]", "") as DATE) AS time_closed,
    ARRAY(
    SELECT
      JSON_EXTRACT_SCALAR(split_items,
        '$.name') AS names
    FROM (
      SELECT
        CONCAT('{', REGEXP_REPLACE(split_items, r'^\[{|}\]$', ''), '}') AS split_items
      FROM
        UNNEST(SPLIT(JSON_EXTRACT(payload,
              '$.issue.labels'), '},{')) AS split_items ) ) AS names
  FROM
    githubarchive.day.20150101
  WHERE
    type="IssuesEvent"
    -- Only want the issue at a specific point otherwise will have duplicates
    AND JSON_EXTRACT(payload,
      '$.action') = "\"closed\"" ) AS tbl
WHERE
  -- the body must be at least 8 words long and the title at least 3 words long
  --  this is an arbitrary way to filter out empty or sparse issues
  ARRAY_LENGTH(SPLIT(body, ' ')) >= 6
  AND ARRAY_LENGTH(SPLIT(title, ' ')) >= 3
  AND ARRAY_LENGTH(names) >= 1
