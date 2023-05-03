USE analysis_basketball_2;

SELECT * FROM leagues;
SELECT * FROM teams;
SELECT * FROM statistics;

INSERT INTO leagues (id_league, name_league)
VALUES (111, 'test');

INSERT INTO teams (id_team_play, date_match, name_team, is_home, total_points, q_1, 
q_2, q_3, q_4, over_time, is_win) VALUES (659, '1993-6-21', 'test name', 1, 158, 45, 
35, 32, 52, 0, 1);

INSERT INTO statistics (id_statistics, avg_gral, mdn_gral, max_gral, min_gral, avg_h,mdn_h, 
max_h, min_h, avg_a, mdn_a, max_a, min_a, avg_q1_h, mdn_q1_h, max_q1_h, min_q1_h, avg_q2_h,
mdn_q2_h, max_q2_h, min_q2_h, avg_q3_h, mdn_q3_h, max_q3_h, min_q3_h, avg_q4_h, mdn_q4_h,
max_q4_h, min_q4_h, avg_q1_a, mdn_q1_a, max_q1_a, min_q1_a, avg_q2_a, mdn_q2_a, max_q2_a,
min_q2_a, avg_q3_a, mdn_q3_a, max_q3_a, min_q3_a, avg_q4_a, mdn_q4_a, max_q4_a, min_q4_a, teams_id_team_play)
VALUES (789, 45.5, 15.054, 145, 4571, 45.5, 15.054, 145, 4571, 45.5, 15.054, 145, 4571, 
45.5, 15.054, 145, 4571, 45.5, 15.054, 145, 4571, 45.5, 15.054, 145, 4571, 45.5, 15.054, 145, 4571,
45.5, 15.054, 145, 4571, 45.5, 15.054, 145, 4571, 45.5, 15.054, 145, 4571, 45.5, 15.054, 145, 4571, 659)