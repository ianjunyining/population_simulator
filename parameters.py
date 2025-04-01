people_at_start = 2
run_similation_days = 365 * 150
health_k_low = -0.00000109589
health_b_low = -0.01
health_k_up = health_k_low
health_b_up = 0.05
health_k_age = -0.00246575342
health_b_age = 100
sudden_death_rate = 3.52837401e-7

# give birth
max_age_give_birth = 50 * 365
min_health_give_birth_wife = 0 # 50
min_health_give_birth_husband = 0 # 20
min_gap_bet_children = 365
max_children_gap = 5 * 365
prob_children_per_day = 1/365 # 1 / (max_children_gap - min_gap_bet_children)

# family
min_age_marry = 18 * 365
marriage_rate = 1
avg_num_children_family = 10
max_num_children_family = 10
