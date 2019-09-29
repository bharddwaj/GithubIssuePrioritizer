SELECT
  *
FROM (
  SELECT
    REGEXP_REPLACE(title, r"\s{2,}", ',') AS issue_title,
    REGEXP_REPLACE(body, r"\s{2,}", ',') AS body,
    ARRAY_TO_STRING(names, ",") AS labels
  FROM (
    SELECT
      LOWER(TRIM(REGEXP_REPLACE(JSON_EXTRACT(payload,
              '$.issue.title'), r"\\n|\(|\)|\[|\]|#|\*|`|\"", ' '))) AS title,
      LOWER(TRIM(REGEXP_REPLACE(JSON_EXTRACT(payload,
              '$.issue.body'), r"\\n|\(|\)|\[|\]|#|\*|`|\"", ' '))) AS body,
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
      `githubarchive.day.2018*`
    WHERE
      type="IssuesEvent"
      -- Only want the issue at a specific point otherwise will have duplicates
      AND JSON_EXTRACT(payload,
        '$.action') = "\"opened\"" ) AS tbl
  WHERE
    -- the body must be at least 8 words long and the title at least 3 words long
    --  this is an arbitrary way to filter out empty or sparse issues
    ARRAY_LENGTH(SPLIT(body, ' ')) >= 6
    AND ARRAY_LENGTH(SPLIT(title, ' ')) >= 3
    AND ARRAY_LENGTH(names) >= 1 )
WHERE
  REGEXP_CONTAINS(lower(labels), "priority")
