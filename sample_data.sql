-- Delete all data from the tables
DELETE FROM flags_activations;

DELETE FROM flags;

DELETE FROM activations;

INSERT INTO activations VALUES(1,'Date Activated','novi.client.activations.date_time_activation.DateTimeActivation','{"startDateTime":"11/26/2023 12:00 AM","endDateTime":"11/28/2023 12:00 AM","format": "%m/%d/%Y %I:%M %p"}');
INSERT INTO activations VALUES(2,'Random Split Activated','novi.client.activations.weighted_random_activation.WeightedRandomActivation','{ "splits":[100, 0, 0], "variations":["A", "B", "C"]}');
INSERT INTO activations VALUES(3,'Combo AND Activation','novi.client.activations.and_activation.AndActivation','[1,2]');
INSERT INTO activations VALUES(4,'Combo OR Activation','novi.client.activations.or_activation.OrActivation','[1,2]');

INSERT INTO flags VALUES(1,'Date Activated Feature',1);
INSERT INTO flags VALUES(2,'Random Variant Feature',1);
INSERT INTO flags VALUES(3,'Combo AND',1);
INSERT INTO flags VALUES(4,'Combo OR',1);

INSERT INTO flags_activations VALUES(1,1);
INSERT INTO flags_activations VALUES(2,2);
INSERT INTO flags_activations VALUES(3,3);
INSERT INTO flags_activations VALUES(4,4);