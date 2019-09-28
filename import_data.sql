-- script based on How To Create Data Products That Are Magical Using Sequence-to-Sequence Models by Hamel Husain
-- gets issues with labels from the Github Archive

SELECT
  url AS issue_url
  -- replace more than one white-space character in a row with a single space
  ,
  REGEXP_REPLACE(title, r"\s{2,}", ' ') AS issue_title,
  REGEXP_REPLACE(body, r"\s{2,}", ' ') AS body,
  names
FROM (
  SELECT
    JSON_EXTRACT(payload,
      '$.issue.html_url') AS url
    --         extract the title and body removing parentheses, brackets, and quotes
    ,
    LOWER(TRIM(REGEXP_REPLACE(JSON_EXTRACT(payload,
            '$.issue.title'), r"\\n|\(|\)|\[|\]|#|\*|`|\"", ' '))) AS title,
    LOWER(TRIM(REGEXP_REPLACE(JSON_EXTRACT(payload,
            '$.issue.body'), r"\\n|\(|\)|\[|\]|#|\*|`|\"", ' '))) AS body,
    LOWER(TRIM(REGEXP_REPLACE(JSON_EXTRACT(payload,
            '$.issue.labels.name'), r"\\n|\(|\)|\[|\]|#|\*|`|\"", ' '))) AS labels,
    ARRAY(
    SELECT
      JSON_EXTRACT_SCALAR(split_items,
        '$.name') AS name
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
  -- filter out issues that have really long titles or bodies
  --    (these are outliers, and will slow tokenization down).
  AND LENGTH(title) <= 400
  AND LENGTH(body) <= 2000
