# simulation
days_in_year = 365
people_at_start = 500
run_similation_days = days_in_year * 1500
window_size_in_days = 30

# person
health_k_low = -0.00000109589
health_b_low = -0.01
health_k_up = health_k_low
health_b_up = 0.05
health_k_age = -0.00246575342
health_b_age = 100
sudden_death_rate = 3.52837401e-7 * window_size_in_days

# give birth
max_age_give_birth = 50 * days_in_year
min_health_give_birth_wife = 50
min_health_give_birth_husband = 20
min_gap_bet_children = days_in_year
max_children_gap = 5 * days_in_year
prob_children_per_window = window_size_in_days / days_in_year # 1 / (max_children_gap - min_gap_bet_children)


# family
min_age_marry = 18 * days_in_year
marriage_rate = 0.8
avg_num_children_family = 2.1
min_num_children_family = 0
max_num_children_family = 7

# negative feedback
enable_negative_feedback = False
stable_population = 1000
avg_num_children_delta = 1e-5 * window_size_in_days
avg_num_children_ub = 2.2
avg_num_children_lb = 2.0
