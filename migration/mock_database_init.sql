-- 1.1. Students Table
INSERT INTO Students (student_id, net_id, first_name, last_name, class_year, email) VALUES
(1001, 'abc123', 'Alice', 'Brown', 2026, 'alice.brown@yale.edu'),
(1002, 'def456', 'David', 'Chen', 2025, 'david.chen@yale.edu'),
(1003, 'ghi789', 'Emma', 'Davis', 2025, 'emma.davis@yale.edu'),
(1004, 'jkl012', 'Frank', 'Garcia', 2026, 'frank.garcia@yale.edu'),
(1005, 'mno345', 'Grace', 'Henderson', 2027, 'grace.henderson@yale.edu');

-- 1.2. Majors Table
INSERT INTO Majors (major_id, major_name, major_code, department, description) VALUES
(101, 'Computer Science', 'CPSC', 'Department of Computer Science', 'The Computer Science major is designed to develop skills in all major areas of computer science while permitting flexibility in exploring particular areas of interest.'),
(102, 'English Language and Literature', 'ENGL', 'Department of English', 'The English major offers a rich and diverse curriculum exploring the history of literature written in English and introducing students to a variety of methods for critical analysis and interpretation.');

-- 1.3. MajorVersions Table
INSERT INTO MajorVersions (major_version_id, major_id, catalog_year, effective_term, valid_until_term, is_active, notes) VALUES
(201, 101, 2023, 'Fall 2023', 'Spring 2027', TRUE, 'Updated CS curriculum with increased emphasis on AI and machine learning.'),
(202, 101, 2022, 'Fall 2022', 'Spring 2026', TRUE, 'Previous CS curriculum.'),
(203, 102, 2023, 'Fall 2023', 'Spring 2027', TRUE, 'Current English major requirements.'),
(204, 102, 2022, 'Fall 2022', 'Spring 2026', TRUE, 'Previous English major requirements.');

-- 1.4. StudentMajors Table
INSERT INTO StudentMajors (student_major_id, student_id, major_version_id, declaration_date, is_primary_major) VALUES
(301, 1001, 201, '2023-05-15', TRUE),  -- Alice: CS Major (primary)
(302, 1002, 201, '2022-10-20', TRUE),  -- David: CS Major (primary)
(303, 1003, 203, '2022-11-10', TRUE),  -- Emma: English Major (primary)
(304, 1004, 201, '2023-04-22', TRUE),  -- Frank: CS Major (primary)
(305, 1004, 203, '2023-04-22', FALSE), -- Frank: English Major (secondary)
(306, 1005, 203, '2024-02-15', TRUE);  -- Grace: English Major (primary)

-- 1.5. Courses Table
-- Computer Science Courses
INSERT INTO Courses (course_id, subject_code, course_number, course_title, description, credits, distribution) VALUES
-- CS Prerequisites
(401, 'CPSC', '112', 'Introduction to Programming', 'An introduction to the concepts, techniques, and applications of computer programming and software development.', 1.0, 'QR'),
(402, 'CPSC', '201', 'Introduction to Computer Science', 'Introduction to the concepts and techniques of computer science.', 1.0, 'QR'),
(403, 'MATH', '112', 'Calculus I', 'Functions, limits, continuity, derivatives, and applications.', 1.0, 'QR'),
(404, 'MATH', '115', 'Calculus II', 'Integration, applications of integration, series, and approximations.', 1.0, 'QR'),
(405, 'MATH', '120', 'Calculus of Functions of Several Variables', 'Multivariable calculus with applications.', 1.0, 'QR'),

-- CS Core Requirements
(406, 'CPSC', '223', 'Data Structures and Programming Techniques', 'Organization of data, algorithms, techniques, and classes.', 1.0, 'QR'),
(407, 'CPSC', '323', 'Systems Programming and Computer Organization', 'Machine architecture, assembly language, and systems programming concepts.', 1.0, 'QR'),
(408, 'CPSC', '365', 'Design and Analysis of Algorithms', 'Paradigms for algorithmic problem solving; algorithms and complexity.', 1.0, 'QR'),
(409, 'CPSC', '366', 'Intensive Algorithms', 'A rigorous introduction to the design and analysis of efficient algorithms.', 1.0, 'QR'),
(410, 'CPSC', '467', 'Cryptography and Computer Security', 'Principles and methods for securing computer systems and data.', 1.0, 'QR'),
(411, 'CPSC', '468', 'Computational Complexity', 'The theory of computational complexity, including NP-completeness.', 1.0, 'QR'),
(412, 'CPSC', '469', 'Randomized Algorithms', 'Design and analysis of randomized algorithms.', 1.0, 'QR'),

-- CS Electives
(413, 'CPSC', '334', 'Creative Embedded Systems', 'Explorations in computer systems with emphasis on physical interaction and creative applications.', 1.0, 'QR'),
(414, 'CPSC', '419', 'Full-Stack Web Programming', 'Building functional and secure web applications from the ground up.', 1.0, 'QR'),
(415, 'CPSC', '422', 'Operating Systems', 'The design and implementation of operating systems.', 1.0, 'QR'),
(416, 'CPSC', '426', 'Building Distributed Systems', 'Architecture and design of modern distributed systems.', 1.0, 'QR'),
(417, 'CPSC', '431', 'Computer Vision and Image Processing', 'Computational approaches to computer vision problems.', 1.0, 'QR'),
(418, 'CPSC', '432', 'Computer-Aided Design of Digital Systems', 'Computer-aided design for digital systems using hardware description languages.', 1.0, 'QR'),
(419, 'CPSC', '436', 'Big Data Systems', 'Design of systems for storing and processing large-scale data.', 1.0, 'QR'),
(420, 'CPSC', '437', 'Database Systems', 'Relational databases, SQL, database design, and implementations.', 1.0, 'QR'),
(421, 'CPSC', '438', 'Applied Cryptography', 'The practice of cryptography and its applications in secure systems.', 1.0, 'QR'),
(422, 'CPSC', '474', 'Computational Intelligence for Games', 'Computational methods for playing and designing games.', 1.0, 'QR'),
(423, 'CPSC', '475', 'Computational Vision and Biological Perception', 'Computational models of human vision.', 1.0, 'QR'),
(424, 'CPSC', '478', 'Computer Graphics', 'The mathematics and computation underlying computer graphics.', 1.0, 'QR'),
(425, 'CPSC', '479', 'Advanced Topics in Computer Graphics', 'Advanced rendering algorithms and applications in computer graphics.', 1.0, 'QR'),
(426, 'CPSC', '483', 'Deep Learning', 'An introduction to deep neural networks and their applications.', 1.0, 'QR'),

-- CS Senior Project
(427, 'CPSC', '490', 'Senior Project', 'Individual research project for seniors majoring in Computer Science.', 1.0, 'QR'),

-- English Courses
-- Introductory and Gateway Courses
(501, 'ENGL', '114', 'Reading and Writing the Modern Essay', 'Close examination of selected literary works with intensive analytical writing.', 1.0, 'WR'),
(502, 'ENGL', '115', 'Literature Seminars', 'Introduction to literary analysis, with an emphasis on practical criticism and close reading.', 1.0, 'Hu'),
(503, 'ENGL', '125', 'Readings in American Literature', 'An introduction to the American literary tradition.', 1.0, 'Hu'),
(504, 'ENGL', '126', 'Readings in British Literature', 'Major works of the British literary tradition from Chaucer to modern times.', 1.0, 'Hu'),
(505, 'ENGL', '127', 'Readings in English Poetry I', 'Major English poets from the medieval period through the eighteenth century.', 1.0, 'Hu'),
(506, 'ENGL', '128', 'Readings in English Poetry II', 'Major English poets from the Romantics through the modern period.', 1.0, 'Hu'),

-- Medieval Period Courses
(507, 'ENGL', '201', 'Medieval Epic and Romance', 'Study of epic and romance traditions in medieval Europe.', 1.0, 'Hu'),
(508, 'ENGL', '205', 'Chaucer''s Canterbury Tales', 'Study of The Canterbury Tales, with emphasis on Chaucer''s language and ethical vision.', 1.0, 'Hu'),

-- Renaissance Period Courses
(509, 'ENGL', '212', 'Shakespeare: The Early Plays', 'A study of Shakespeare''s comedies, histories, and early tragedies.', 1.0, 'Hu'),
(510, 'ENGL', '213', 'Shakespeare: The Later Plays', 'A study of Shakespeare''s later tragedies and romances.', 1.0, 'Hu'),
(511, 'ENGL', '220', 'Milton', 'A study of Milton''s poetry, with some attention to his literary sources, contexts, and prose.', 1.0, 'Hu'),

-- 18th-19th Century Courses
(512, 'ENGL', '234', 'The Eighteenth-Century Novel', 'The rise of the novel as a genre in the eighteenth century.', 1.0, 'Hu'),
(513, 'ENGL', '248', 'Romanticism and Revolution', 'Major works of the British Romantic poets in the context of political and social revolution.', 1.0, 'Hu'),
(514, 'ENGL', '253', 'The American Novel Since 1945', 'American novels from the late 1940s to the present.', 1.0, 'Hu'),
(515, 'ENGL', '265', 'Victorian Poetry', 'Major works by Victorian poets, with emphasis on historical context and poetic form.', 1.0, 'Hu'),

-- Modern and Contemporary Courses
(516, 'ENGL', '283', 'Modernism', 'Aspects of British and American modernism in the early twentieth century.', 1.0, 'Hu'),
(517, 'ENGL', '290', 'Postcolonial Literature', 'Literature from colonial and postcolonial contexts.', 1.0, 'Hu'),
(518, 'ENGL', '300', 'Contemporary American Literature', 'American literature from the late twentieth and early twenty-first centuries.', 1.0, 'Hu'),

-- Advanced Seminars and Workshops
(519, 'ENGL', '450', 'Advanced Seminar in Literary Theory', 'Intensive study of literary theory and methodologies.', 1.0, 'Hu'),
(520, 'ENGL', '470', 'Senior Essay for English Majors', 'Independent research and writing on a topic of the student''s choice.', 1.0, 'Hu');

-- 1.6. StudentCourseEnrollments Table
INSERT INTO StudentCourseEnrollments (enrollment_id, student_id, course_id, term_taken, grade, status) VALUES
-- Alice (CS Major)
(601, 1001, 401, 'Fall 2022', 'A', 'Completed'),  -- Intro to Programming
(602, 1001, 403, 'Fall 2022', 'A-', 'Completed'), -- Calculus I
(603, 1001, 404, 'Spring 2023', 'B+', 'Completed'), -- Calculus II
(604, 1001, 402, 'Spring 2023', 'A', 'Completed'), -- Intro to CS
(605, 1001, 406, 'Fall 2023', 'B+', 'Completed'), -- Data Structures
(606, 1001, 407, 'Spring 2024', 'A-', 'Completed'), -- Systems Programming
(607, 1001, 414, 'Fall 2024', 'A', 'Enrolled'),   -- Web Programming
(608, 1001, 408, 'Fall 2024', 'B+', 'Enrolled'),  -- Algorithms

-- David (CS Major)
(609, 1002, 401, 'Fall 2021', 'A-', 'Completed'), -- Intro to Programming
(610, 1002, 402, 'Spring 2022', 'A', 'Completed'), -- Intro to CS
(611, 1002, 403, 'Fall 2022', 'B+', 'Completed'), -- Calculus I
(612, 1002, 404, 'Spring 2023', 'B', 'Completed'), -- Calculus II
(613, 1002, 406, 'Fall 2022', 'A-', 'Completed'), -- Data Structures
(614, 1002, 407, 'Spring 2023', 'B+', 'Completed'), -- Systems Programming
(615, 1002, 408, 'Fall 2023', 'A', 'Completed'),  -- Algorithms
(616, 1002, 415, 'Spring 2024', 'A-', 'Completed'), -- Operating Systems
(617, 1002, 420, 'Fall 2024', NULL, 'Enrolled'),  -- Database Systems
(618, 1002, 421, 'Fall 2024', NULL, 'Enrolled'),  -- Applied Cryptography

-- Emma (English Major)
(619, 1003, 502, 'Fall 2021', 'A', 'Completed'),  -- Literature Seminars
(620, 1003, 504, 'Spring 2022', 'A-', 'Completed'), -- Readings in British Lit
(621, 1003, 503, 'Fall 2022', 'B+', 'Completed'), -- Readings in American Lit
(622, 1003, 509, 'Spring 2023', 'A', 'Completed'), -- Shakespeare: Early Plays
(623, 1003, 513, 'Fall 2023', 'A-', 'Completed'), -- Romanticism
(624, 1003, 516, 'Spring 2024', 'A', 'Completed'), -- Modernism
(625, 1003, 517, 'Fall 2024', NULL, 'Enrolled'),  -- Postcolonial Literature
(626, 1003, 519, 'Fall 2024', NULL, 'Enrolled'),  -- Advanced Literary Theory

-- Frank (Double Major: CS and English)
(627, 1004, 401, 'Fall 2022', 'A-', 'Completed'), -- Intro to Programming
(628, 1004, 402, 'Spring 2023', 'B+', 'Completed'), -- Intro to CS
(629, 1004, 403, 'Fall 2022', 'B', 'Completed'),  -- Calculus I
(630, 1004, 404, 'Spring 2023', 'B-', 'Completed'), -- Calculus II
(631, 1004, 502, 'Fall 2022', 'A', 'Completed'),  -- Literature Seminars
(632, 1004, 503, 'Spring 2023', 'A-', 'Completed'), -- Readings in American Lit
(633, 1004, 406, 'Fall 2023', 'B+', 'Completed'), -- Data Structures
(634, 1004, 509, 'Fall 2023', 'A', 'Completed'),  -- Shakespeare: Early Plays
(635, 1004, 407, 'Spring 2024', 'B+', 'Completed'), -- Systems Programming
(636, 1004, 513, 'Spring 2024', 'A-', 'Completed'), -- Romanticism
(637, 1004, 408, 'Fall 2024', NULL, 'Enrolled'),  -- Algorithms
(638, 1004, 516, 'Fall 2024', NULL, 'Enrolled'),  -- Modernism

-- Grace (English Major)
(639, 1005, 502, 'Fall 2023', 'A-', 'Completed'), -- Literature Seminars
(640, 1005, 503, 'Fall 2023', 'B+', 'Completed'), -- Readings in American Lit
(641, 1005, 504, 'Spring 2024', 'A', 'Completed'), -- Readings in British Lit
(642, 1005, 505, 'Spring 2024', 'A-', 'Completed'), -- Readings in English Poetry I
(643, 1005, 509, 'Fall 2024', NULL, 'Enrolled'),  -- Shakespeare: Early Plays
(644, 1005, 512, 'Fall 2024', NULL, 'Enrolled');  -- 18th-Century Novel

-- 1.7. StudentCoursePlans Table
INSERT INTO StudentCoursePlans (plan_id, student_id, course_id, intended_term, priority, notes) VALUES
-- Alice (CS Major)
(701, 1001, 426, 'Spring 2025', 1, 'Interested in AI focus'),
(702, 1001, 427, 'Fall 2025', 1, 'Required for graduation'),
(703, 1001, 417, 'Fall 2025', 2, 'Considering computer vision track'),
(704, 1001, 422, 'Spring 2026', 2, 'Gaming interests'),

-- David (CS Major)
(705, 1002, 426, 'Spring 2025', 1, 'AI focus'),
(706, 1002, 427, 'Fall 2025', 1, 'Senior project'),

-- Emma (English Major)
(707, 1003, 510, 'Spring 2025', 1, 'Complete Shakespeare requirement'),
(708, 1003, 520, 'Fall 2025', 1, 'Senior essay'),

-- Frank (Double Major)
(709, 1004, 427, 'Spring 2025', 1, 'CS senior project'),
(710, 1004, 520, 'Spring 2025', 1, 'English senior essay'),
(711, 1004, 424, 'Fall 2025', 2, 'Interest in graphics'),

-- Grace (English Major)
(712, 1005, 510, 'Spring 2025', 1, 'Complete Shakespeare'),
(713, 1005, 513, 'Spring 2025', 2, 'Fulfill British lit requirement'),
(714, 1005, 517, 'Fall 2025', 1, 'Interest in postcolonial studies');

-- 1.8. MajorRequirements Table
-- Computer Science Major Requirements
INSERT INTO MajorRequirements (requirement_id, major_version_id, requirement_name, requirement_type, description, min_credits, max_credits, min_courses, max_courses) VALUES
-- CS Requirements
(801, 201, 'Prerequisites', 'Prerequisite', 'Foundational courses required before declaring the CS major', 0, 0, 3, 3),
(802, 201, 'Core Requirements', 'Core', 'Required courses for all CS majors', 0, 0, 3, 3),
(803, 201, 'Advanced Electives', 'Elective', 'Upper-level CS courses in various specializations', 0, 0, 6, NULL),
(804, 201, 'Senior Project', 'Capstone', 'Individual research project in computer science', 0, 0, 1, 1),

-- English Major Requirements
(805, 203, 'Foundational Courses', 'Prerequisite', 'Gateway courses for the English major', 0, 0, 3, 3),
(806, 203, 'Historical Distribution', 'Core', 'Courses representing different historical periods', 0, 0, 4, NULL),
(807, 203, 'Advanced Seminars', 'Core', 'Upper-level seminars in literary studies', 0, 0, 2, NULL),
(808, 203, 'Senior Essay', 'Capstone', 'Independent research and writing project', 0, 0, 1, 1),
(809, 203, 'Electives', 'Elective', 'Additional courses in English', 0, 0, 2, NULL);

-- 1.9. RequirementGroups Table
INSERT INTO RequirementGroups (requirement_group_id, requirement_id, group_name, group_operator, min_courses_in_group, max_courses_in_group, group_description) VALUES
-- Computer Science Groups
-- Prerequisites
(901, 801, 'Introductory Programming', 'OR', 1, 1, 'Introductory programming requirement'),
(902, 801, 'Intro to Computer Science', 'OR', 1, 1, 'Introduction to computer science theory'),
(903, 801, 'Mathematics', 'OR', 1, 1, 'Mathematical foundations'),

-- Core Requirements
(904, 802, 'Software Development', 'OR', 1, 1, 'Programming techniques and data structures'),
(905, 802, 'Computer Organization', 'OR', 1, 1, 'Computer architecture and systems'),
(906, 802, 'Algorithms', 'OR', 1, 1, 'Analysis of algorithms'),

-- Advanced Electives
(907, 803, 'Systems', 'OR', 1, NULL, 'Systems, networking, and security'),
(908, 803, 'Theory', 'OR', 1, NULL, 'Theoretical computer science'),
(909, 803, 'Application', 'OR', 1, NULL, 'Applications of computer science'),
(910, 803, 'AI and ML', 'OR', 1, NULL, 'Artificial intelligence and machine learning'),

-- Senior Project
(911, 804, 'Senior Project', 'OR', 1, 1, 'Required senior project'),

-- English Groups
-- Foundational Courses
(912, 805, 'Literature Seminars', 'OR', 1, 1, 'Introductory literature seminars'),
(913, 805, 'Readings in Literature', 'OR', 2, 2, 'Survey courses in English and American literature'),

-- Historical Distribution
(914, 806, 'Medieval Period', 'OR', 1, 1, 'Medieval literature (before 1500)'),
(915, 806, 'Renaissance Period', 'OR', 1, 1, 'Renaissance literature (1500-1660)'),
(916, 806, '18th-19th Century', 'OR', 1, 1, 'Literature from 1660-1900'),
(917, 806, 'Modern/Contemporary', 'OR', 1, 1, 'Literature from 1900-present'),

-- Advanced Seminars
(918, 807, 'Advanced Seminars', 'OR', 2, 2, 'Upper-level English courses'),

-- Senior Essay
(919, 808, 'Senior Essay', 'OR', 1, 1, 'Required senior essay'),

-- Electives
(920, 809, 'Additional English Courses', 'OR', 2, NULL, 'Any additional English department courses');

-- 1.10. RequirementGroupCourses Table
INSERT INTO RequirementGroupCourses (req_group_course_id, requirement_group_id, course_id, is_required_in_group) VALUES
-- Computer Science
-- Introductory Programming
(1001, 901, 401, FALSE),  -- CPSC 112: Intro to Programming

-- Intro to Computer Science
(1002, 902, 402, FALSE),  -- CPSC 201: Intro to Computer Science

-- Mathematics
(1003, 903, 403, FALSE),  -- MATH 112: Calculus I
(1004, 903, 404, FALSE),  -- MATH 115: Calculus II
(1005, 903, 405, FALSE),  -- MATH 120: Multivariable Calculus

-- Software Development
(1006, 904, 406, FALSE),  -- CPSC 223: Data Structures

-- Computer Organization
(1007, 905, 407, FALSE),  -- CPSC 323: Systems Programming

-- Algorithms
(1008, 906, 408, FALSE),  -- CPSC 365: Algorithms
(1009, 906, 409, FALSE),  -- CPSC 366: Intensive Algorithms

-- Systems
(1010, 907, 410, FALSE),  -- CPSC 467: Cryptography
(1011, 907, 415, FALSE),  -- CPSC 422: Operating Systems
(1012, 907, 416, FALSE),  -- CPSC 426: Distributed Systems
(1013, 907, 419, FALSE),  -- CPSC 436: Big Data Systems
(1014, 907, 420, FALSE),  -- CPSC 437: Database Systems
(1015, 907, 421, FALSE),  -- CPSC 438: Applied Cryptography

-- Theory
(1016, 908, 410, FALSE),  -- CPSC 467: Cryptography (also appears in Systems)
(1017, 908, 411, FALSE),  -- CPSC 468: Computational Complexity
(1018, 908, 412, FALSE),  -- CPSC 469: Randomized Algorithms

-- Application
(1019, 909, 413, FALSE),  -- CPSC 334: Creative Embedded Systems
(1020, 909, 414, FALSE),  -- CPSC 419: Full-Stack Web Programming
(1021, 909, 417, FALSE),  -- CPSC 431: Computer Vision
(1022, 909, 418, FALSE),  -- CPSC 432: Digital Systems
(1023, 909, 422, FALSE),  -- CPSC 474: Games
(1024, 909, 424, FALSE),  -- CPSC 478: Computer Graphics
(1025, 909, 425, FALSE),  -- CPSC 479: Advanced Graphics

-- AI and ML
(1026, 910, 423, FALSE),  -- CPSC 475: Computational Vision
(1027, 910, 426, FALSE),  -- CPSC 483: Deep Learning

-- Senior Project
(1028, 911, 427, TRUE),   -- CPSC 490: Senior Project

-- English
-- Literature Seminars
(1029, 912, 502, FALSE),  -- ENGL 115: Literature Seminars

-- Readings in Literature
(1030, 913, 503, FALSE),  -- ENGL 125: American Literature
(1031, 913, 504, FALSE),  -- ENGL 126: British Literature
(1032, 913, 505, FALSE),  -- ENGL 127: English Poetry I
(1033, 913, 506, FALSE),  -- ENGL 128: English Poetry II

-- Medieval Period
(1034, 914, 507, FALSE),  -- ENGL 201: Medieval Epic
(1035, 914, 508, FALSE),  -- ENGL 205: Chaucer

-- Renaissance Period
(1036, 915, 509, FALSE),  -- ENGL 212: Shakespeare Early
(1037, 915, 510, FALSE),  -- ENGL 213: Shakespeare Later
(1038, 915, 511, FALSE),  -- ENGL 220: Milton

-- 18th-19th Century
(1039, 916, 512, FALSE),  -- ENGL 234: 18th Century Novel
(1040, 916, 513, FALSE),  -- ENGL 248: Romanticism
(1041, 916, 514, FALSE),  -- ENGL 253: American Novel
(1042, 916, 515, FALSE),  -- ENGL 265: Victorian Poetry

-- Modern/Contemporary
(1043, 917, 516, FALSE),  -- ENGL 283: Modernism
(1044, 917, 517, FALSE),  -- ENGL 290: Postcolonial
(1045, 917, 518, FALSE),  -- ENGL 300: Contemporary American

-- Advanced Seminars
(1046, 918, 519, FALSE),  -- ENGL 450: Literary Theory

-- Senior Essay
(1047, 919, 520, TRUE),   -- ENGL 470: Senior Essay

-- Electives (all courses can count as electives)
(1048, 920, 503, FALSE),
(1049, 920, 504, FALSE),
(1050, 920, 505, FALSE),
(1051, 920, 506, FALSE),
(1052, 920, 507, FALSE),
(1053, 920, 508, FALSE),
(1054, 920, 509, FALSE),
(1055, 920, 510, FALSE),
(1056, 920, 511, FALSE),
(1057, 920, 512, FALSE),
(1058, 920, 513, FALSE),
(1059, 920, 514, FALSE),
(1060, 920, 515, FALSE),
(1061, 920, 516, FALSE),
(1062, 920, 517, FALSE),
(1063, 920, 518, FALSE),
(1064, 920, 519, FALSE);


-- 1.11. RequirementRules Table (for Advanced Logic)
INSERT INTO RequirementRules (requirement_rule_id, requirement_id, requirement_group_id, rule_type, operator, value, notes) VALUES
-- Computer Science Rules
-- Core Requirements need minimum B- grade
(1101, 802, NULL, 'MIN_GRADE', '>=', 'B-', 'Core courses must be passed with B- or better'),
-- Advanced Electives: Need minimum of 4 at 400-level or above
(1102, 803, NULL, 'COURSE_LEVEL', '>=', '400', 'At least 4 electives must be at the 400 level'),
-- One theory course needed
(1103, NULL, 908, 'MIN_COURSES', '>=', '1', 'At least one theory course is required'),
-- Senior Project needs instructor permission
(1104, 804, NULL, 'INSTRUCTOR_PERMISSION', '=', 'TRUE', 'Senior project requires instructor permission'),

-- English Rules
-- Minimum of one course with a writing-intensive component
(1105, 805, NULL, 'DISTRIBUTION_REQUIRED', '=', 'WR', 'At least one foundational course must fulfill writing requirement'),
-- Need at least one course from each major literary period
(1106, 806, NULL, 'DISTRIBUTION_COVERAGE', '=', 'TRUE', 'At least one course from each major period'),
-- Advanced Seminars must be junior or senior standing
(1107, 807, NULL, 'CLASS_STANDING', '>=', 'Junior', 'Advanced seminars require junior or senior standing'),
-- Minimum of 2 courses must be focused on literature pre-1800
(1108, 806, NULL, 'PERIOD_COVERAGE', '<=', '1800', 'At least 2 courses must cover pre-1800 literature'),
-- Need minimum of 12 total English courses for the major
(1109, NULL, NULL, 'TOTAL_COURSES', '>=', '12', 'Total of 12 courses required for the major');

-- 1.12. CoursePrerequisites Table
INSERT INTO CoursePrerequisites (course_id, prereq_course_id, concurrency_allowed) VALUES
-- Computer Science Prerequisites
(406, 401, FALSE),  -- Data Structures requires Intro to Programming
(406, 402, FALSE),  -- Data Structures requires Intro to CS
(407, 406, FALSE),  -- Systems Programming requires Data Structures
(408, 406, FALSE),  -- Algorithms requires Data Structures
(409, 406, FALSE),  -- Intensive Algorithms requires Data Structures
(409, 404, FALSE),  -- Intensive Algorithms requires Calculus II
(410, 408, FALSE),  -- Cryptography requires Algorithms
(411, 408, FALSE),  -- Computational Complexity requires Algorithms
(412, 408, FALSE),  -- Randomized Algorithms requires Algorithms
(413, 406, FALSE),  -- Creative Embedded Systems requires Data Structures
(414, 406, FALSE),  -- Web Programming requires Data Structures
(415, 407, FALSE),  -- Operating Systems requires Systems Programming
(416, 407, FALSE),  -- Distributed Systems requires Systems Programming
(417, 406, FALSE),  -- Computer Vision requires Data Structures
(418, 407, FALSE),  -- Digital Systems requires Systems Programming
(419, 406, FALSE),  -- Big Data Systems requires Data Structures
(420, 406, FALSE),  -- Database Systems requires Data Structures
(421, 410, FALSE),  -- Applied Cryptography requires Cryptography
(422, 406, FALSE),  -- Games requires Data Structures
(423, 417, FALSE),  -- Computational Vision requires Computer Vision
(424, 406, FALSE),  -- Computer Graphics requires Data Structures
(425, 424, FALSE),  -- Advanced Graphics requires Computer Graphics
(426, 406, FALSE),  -- Deep Learning requires Data Structures
(427, 408, FALSE),  -- Senior Project requires Algorithms

-- English Prerequisites
(507, 502, FALSE),  -- Medieval Epic requires Literature Seminars
(508, 502, FALSE),  -- Chaucer requires Literature Seminars
(509, 502, FALSE),  -- Shakespeare Early requires Literature Seminars
(510, 502, FALSE),  -- Shakespeare Later requires Literature Seminars
(510, 509, FALSE),  -- Shakespeare Later typically follows Shakespeare Early
(511, 502, FALSE),  -- Milton requires Literature Seminars
(512, 502, FALSE),  -- 18th Century Novel requires Literature Seminars
(513, 502, FALSE),  -- Romanticism requires Literature Seminars
(514, 502, FALSE),  -- American Novel requires Literature Seminars
(514, 503, FALSE),  -- American Novel requires Readings in American Literature
(515, 502, FALSE),  -- Victorian Poetry requires Literature Seminars
(516, 502, FALSE),  -- Modernism requires Literature Seminars
(517, 502, FALSE),  -- Postcolonial requires Literature Seminars
(518, 502, FALSE),  -- Contemporary American requires Literature Seminars
(518, 503, FALSE),  -- Contemporary American requires Readings in American Literature
(519, 502, FALSE),  -- Literary Theory requires Literature Seminars
(520, 519, FALSE);  -- Senior Essay requires Advanced Seminar in Literary Theory

-- 1.13. EquivalenceGroups Table
INSERT INTO EquivalenceGroups (eq_group_id, group_name, group_notes) VALUES
(1301, 'Introductory Programming Equivalents', 'Courses that satisfy the introductory programming requirement'),
(1302, 'Shakespeare Course Equivalents', 'Courses that fulfill the Shakespeare requirement'),
(1303, 'Advanced Math Equivalents', 'Higher-level math courses that can substitute for the calculus requirement'),
(1304, 'Literary Theory Equivalents', 'Courses that address literary theory requirements');

-- 1.14. EquivalenceGroupCourses Table
INSERT INTO EquivalenceGroupCourses (eq_group_course_id, eq_group_id, course_id) VALUES
-- Programming Equivalents
(1401, 1301, 401),  -- CPSC 112: Intro to Programming (canonical course)
(1402, 1301, 414),  -- CPSC 419: Web Programming (can substitute in some cases)

-- Shakespeare Equivalents
(1403, 1302, 509),  -- ENGL 212: Shakespeare Early (canonical course)
(1404, 1302, 510),  -- ENGL 213: Shakespeare Later

-- Math Equivalents
(1405, 1303, 403),  -- MATH 112: Calculus I (canonical course)
(1406, 1303, 404),  -- MATH 115: Calculus II
(1407, 1303, 405),  -- MATH 120: Multivariable Calculus

-- Literary Theory Equivalents
(1408, 1304, 519),  -- ENGL 450: Literary Theory (canonical course)
(1409, 1304, 517);  -- ENGL 290: Postcolonial (has theory component)

-- Distribution Type definitions
CREATE TABLE DistributionTypes (
    distribution_id SERIAL PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(20) NOT NULL  -- 'skills' or 'disciplinary'
);

-- Insert distribution types
INSERT INTO DistributionTypes (code, name, description, category) VALUES
('QR', 'Quantitative Reasoning', 'Courses developing quantitative reasoning skills', 'skills'),
('WR', 'Writing', 'Courses developing writing skills', 'skills'),
('L', 'Foreign Language', 'Courses developing proficiency in a foreign language', 'skills'),
('Hu', 'Humanities and Arts', 'Courses in humanities and arts', 'disciplinary'),
('Sc', 'Science', 'Courses in science', 'disciplinary'),
('So', 'Social Science', 'Courses in social science', 'disciplinary');

-- Academic year definitions
CREATE TABLE AcademicYears (
    year_id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,  -- 'Freshman', 'Sophomore', etc.
    display_order INTEGER NOT NULL,    -- For ordering (1, 2, 3, 4)
    description TEXT
);

-- Insert academic years
INSERT INTO AcademicYears (name, display_order, description) VALUES
('Freshman', 1, '1 course in two of three skills categories'),
('Sophomore', 2, '1 course in each disciplinary area and each skills category'),
('Junior', 3, 'Complete all skills requirements'),
('Senior', 4, 'Complete all distributional requirements');

-- Year-specific distribution requirements
CREATE TABLE DistributionRequirements (
    requirement_id SERIAL PRIMARY KEY,
    year_id INTEGER REFERENCES AcademicYears(year_id),
    distribution_id INTEGER REFERENCES DistributionTypes(distribution_id),
    courses_required INTEGER NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Special year requirements (like "2 of 3 categories")
CREATE TABLE YearRequirementRules (
    rule_id SERIAL PRIMARY KEY,
    year_id INTEGER REFERENCES AcademicYears(year_id),
    rule_type VARCHAR(50) NOT NULL,  -- e.g., 'MIN_CATEGORIES'
    value INTEGER NOT NULL,          -- e.g., 2 (for "2 of 3 categories")
    category VARCHAR(20),            -- e.g., 'skills' (to specify only skills categories)
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert distribution requirements for each year
-- We now let the database handle the requirement_id auto-incrementing
INSERT INTO DistributionRequirements (year_id, distribution_id, courses_required) VALUES
-- Freshman requirements (using sequence numbers from the inserts above)
(1, 1, 1),  -- QR: 1 course
(1, 2, 1),  -- WR: 1 course
(1, 3, 1),  -- L: 1 course
-- Sophomore requirements
(2, 1, 1),  -- QR: 1 course
(2, 2, 1),  -- WR: 1 course
(2, 3, 1),  -- L: 1 course
(2, 4, 1),  -- Hu: 1 course
(2, 5, 1),  -- Sc: 1 course
(2, 6, 1),  -- So: 1 course
-- Junior requirements
(3, 1, 2),  -- QR: 2 courses
(3, 2, 2),  -- WR: 2 courses
(3, 3, 1),  -- L: 1 course
(3, 4, 1),  -- Hu: 1 course
(3, 5, 1),  -- Sc: 1 course
(3, 6, 1),  -- So: 1 course
-- Senior requirements
(4, 1, 2),  -- QR: 2 courses
(4, 2, 2),  -- WR: 2 courses
(4, 3, 1),  -- L: 1 course
(4, 4, 2),  -- Hu: 2 courses
(4, 5, 2),  -- Sc: 2 courses
(4, 6, 2);  -- So: 2 courses

-- Insert special rules for each year
INSERT INTO YearRequirementRules (year_id, rule_type, value, category) VALUES
-- Freshman Year: Need 2 of 3 skills categories
(1, 'MIN_CATEGORIES', 2, 'skills'),  -- Need at least 2 skills categories

-- Sophomore Year: Need all categories (both skills and disciplinary)
(2, 'MIN_CATEGORIES', 6, NULL),      -- Need all 6 categories (3 skills + 3 disciplinary)
(2, 'MIN_SKILLS_CATEGORIES', 3, 'skills'),    -- Need all 3 skills categories
(2, 'MIN_DISCIPLINARY_CATEGORIES', 3, 'disciplinary'), -- Need all 3 disciplinary categories

-- Junior Year: Complete skills requirements and maintain disciplinary minimums
(3, 'MIN_CATEGORIES', 6, NULL),      -- Still need all 6 categories
(3, 'COMPLETE_SKILLS', 1, 'skills'), -- Must have completed skills requirements
(3, 'MIN_DISCIPLINARY_CATEGORIES', 3, 'disciplinary'), -- Still need all 3 disciplinary areas

-- Senior Year: Complete all requirements 
(4, 'MIN_CATEGORIES', 6, NULL),      -- Need all 6 categories
(4, 'COMPLETE_SKILLS', 1, 'skills'), -- Must have completed skills requirements
(4, 'COMPLETE_DISCIPLINARY', 1, 'disciplinary'); -- Must have completed disciplinary requirements