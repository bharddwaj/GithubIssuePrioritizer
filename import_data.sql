SELECT
  *
FROM (
  SELECT
    REGEXP_REPLACE(title, r"\s{2,}", ',') AS issue_title,
    REGEXP_REPLACE(body, r"\s{2,}", ',') AS body,
    (
    SELECT
      REGEXP_REPLACE(LOWER(name), r'[^0-9a-zA-Z ]', " ")
    FROM
      UNNEST(names) AS name
    WHERE
      REGEXP_CONTAINS(LOWER(name), "priority")
    LIMIT
      1) AS priority,
    REGEXP_REPLACE(ARRAY_TO_STRING(ARRAY(
        SELECT
          LOWER(name)
        FROM
          UNNEST(names) AS name
        WHERE
          NOT REGEXP_CONTAINS(LOWER(name), "priority")), ","), r'[^0-9a-zA-Z ]', " ") AS other_labels
  FROM (
    SELECT
      LOWER(TRIM(REGEXP_REPLACE(JSON_EXTRACT(payload,
              '$.issue.title'), r"\\n|\(|\)|\[|\]|#|\*|`|\"", ' '))) AS title,
      LOWER(TRIM(REGEXP_REPLACE(JSON_EXTRACT(payload,
              '$.issue.body'), r"\\n|\(|\)|\[|\]|#|\*|`|\"", ' '))) AS body,
      ARRAY(
      SELECT
        JSON_EXTRACT_SCALAR(split_items,
          '$.name')
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
  priority IS NOT NULL
