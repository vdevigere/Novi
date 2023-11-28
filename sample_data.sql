-- Delete all data from the tables
DELETE FROM flags_activations;

DELETE FROM flags;

DELETE FROM activations;

-- Seed the flags table
INSERT INTO flags
            (name,
             status)
VALUES     ('Date Activated Feature',
            TRUE);

INSERT INTO flags
            (name,
             status)
VALUES     ('Random Variant Feature',
            TRUE);


-- Seed the activations table
INSERT INTO activations
            (name,
			class_name,
             config)
VALUES     ("Date Activated",
			"novi_activations.standard.date_time_activation.DateTimeActivation",
            '{"startDateTime":"11/26/2023 12:00 AM","endDateTime":"11/28/2023 12:00 AM","format": "%m/%d/%Y %I:%M %p"}'
            );

INSERT INTO activations
            (name,
			class_name,
             config)
VALUES     ("Random Split Activated",
			"novi_activations.standard.weighted_random_activation.WeightedRandomActivation",
            '{ "splits":[100, 0, 0], "variations":["A", "B", "C"]}');

-- Seed the flags_activations table
INSERT INTO flags_activations
            (flag_id,
             activation_id)
SELECT flags.id,
       activations.id
FROM   flags,
       activations
WHERE  flags.name == 'Date Activated Feature'
       AND activations.name = 'Date Activated';

INSERT INTO flags_activations
            (flag_id,
             activation_id)
SELECT flags.id,
       activations.id
FROM   flags,
       activations
WHERE  flags.name == 'Random Variant Feature'
       AND activations.name = 'Random Split Activated';