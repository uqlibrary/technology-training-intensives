#### Project 1 - Analysing coffee data #####


library(dplyr)
library(readr)
library(ggplot2)
install.packages("plot_ly")
install.packages("plotly")

coffee <- read_csv("data/coffee_survey.csv")

head(coffee)
str(coffee)

ggplot(coffee, aes(x = age, y = favourite, color = cups)) +
  geom_count()

ggplot(coffee, aes(x = age, y = cups)) +
  geom_count()

ggplot(coffee, aes(x = cups, y = age)) +
  geom_count()


ggplot(coffee, aes(x = favourite, y = cups)) +
  geom_count()

ggplot(coffee, aes(x = favourite, y = cups)) +
  geom_bar()

names(coffee$favourite)

ggplot(coffee, aes( y = ))


unique(coffee$favourite)
unqiue(coffee)

ggplot(coffee, aes(x = age, y = prefer_overall))+
  geom_count()


# which age group has a prefence for which coffee


##pivot

library(dplyr)
library(tidyr)

coffee_acidity_long <- coffee %>%
  pivot_longer(
    cols = starts_with("coffee_") & ends_with("_acidity"),
    names_to = "coffee",
    values_to = "acidity"
  )

# add labels

coffee_acidity_long <- coffee_acidity_long %>%
  mutate(
    coffee = recode(coffee,
                    coffee_a_acidity = "Coffee A",
                    coffee_b_acidity = "Coffee B",
                    coffee_c_acidity = "Coffee C",
                    coffee_d_acidity = "Coffee D"
    )
  )

# remove NA

coffee_acidity_long <- coffee_acidity_long %>%
  filter(!is.na(acidity))

# plot

ggplot(coffee_acidity_long, aes(x = coffee, y = acidity)) +
  geom_boxplot() +
  labs(
    x = "Coffee",
    y = "Acidity rating",
    title = "Perceived acidity of coffees A–D"
  ) +
  theme_minimal()



## taking the mean of acidity

coffee_acidity_long %>%
  group_by(coffee) %>%
  summarise(
    mean_acidity = mean(acidity),
    se = sd(acidity) / sqrt(n()),
    .groups = "drop"
  ) %>%
  ggplot(aes(coffee, mean_acidity)) +
  geom_col() +
  geom_errorbar(
    aes(ymin = mean_acidity - se, ymax = mean_acidity + se),
    width = 0.2
  ) +
  labs(y = "Mean acidity rating") +
  theme_minimal()



### compare bitterness and acidity


coffee_ba <- coffee %>%
  pivot_longer(
    cols = matches("^coffee_[abcd]_(bitterness|acidity)$"),
    names_to = c("coffee", "metric"),
    names_pattern = "^coffee_([abcd])_(bitterness|acidity)$",
    values_to = "score"
  ) %>%
  mutate(
    coffee = paste("Coffee", toupper(coffee))
  ) %>%
  pivot_wider(
    names_from = metric,
    values_from = score
  ) %>%
  filter(!is.na(bitterness), !is.na(acidity))

ggplot(coffee_ba, aes(x = acidity, y = bitterness, color = coffee)) +
  geom_point(alpha = 0.4) +
  geom_smooth(method = "lm", se = FALSE) +
  facet_wrap(~ coffee) +
  labs(
    x = "Acidity rating",
    y = "Bitterness rating",
    title = "Bitterness vs acidity by coffee"
  ) +
  theme_minimal()



coffee_scores <- coffee %>%
  pivot_longer(
    cols = matches("^coffee_[abcd]_(bitterness|acidity)$"),
    names_to = c("coffee", "metric"),
    names_pattern = "^coffee_([abcd])_(bitterness|acidity)$",
    values_to = "score"
  ) %>%
  filter(!is.na(score)) %>%
  mutate(coffee = paste("Coffee", toupper(coffee))) %>%
  group_by(coffee, metric) %>%
  summarise(
    mean_score = mean(score),
    se = sd(score) / sqrt(n()),
    n = n(),
    .groups = "drop"
  ) %>%
  pivot_wider(
    names_from = metric,
    values_from = c(mean_score, se, n)
  )
coffee_scores <- coffee_scores %>%
  rename(
    mean_acidity    = mean_score_acidity,
    mean_bitterness = mean_score_bitterness
  )


ggplot(coffee_scores, aes(x = mean_acidity, y = mean_bitterness, label = coffee)) +
  geom_point(size = 4) +
  geom_errorbar(
    aes(
      ymin = mean_bitterness - se_bitterness,
      ymax = mean_bitterness + se_bitterness
    ),
    width = 0
  ) +
  geom_errorbarh(
    aes(
      xmin = mean_acidity - se_acidity,
      xmax = mean_acidity + se_acidity
    ),
    height = 0
  ) +
  geom_text(vjust = -1) +
  labs(
    x = "Mean perceived acidity",
    y = "Mean perceived bitterness",
    title = "Average perceived acidity and bitterness of coffees"
  ) +
  theme_minimal()

## determine coffee popularity


coffee_pref_counts <- coffee %>%
  filter(!is.na(prefer_overall)) %>%
  count(prefer_overall, name = "n_prefer") %>%
  rename(coffee = prefer_overall)

# join to new coffee dataframe

coffee_scores <- coffee_scores %>%
  left_join(coffee_pref_counts, by = "coffee")



# plot with symbol size = popularity

ggplot(
  coffee_scores,
  aes(
    x = mean_acidity,
    y = mean_bitterness,
    size = n_prefer,
    label = coffee
  )
) +
  geom_point(alpha = 0.7) +
  geom_text(vjust = -1) +
  scale_size_continuous(
    name = "Number of respondents\npreferring this coffee"
  ) +
  labs(
    x = "Mean perceived acidity",
    y = "Mean perceived bitterness",
    title = "Coffee flavor space with popularity-weighted symbols"
  ) +
  theme_minimal()

# label coffees with color instead of text

ggplot(
  coffee_scores,
  aes(
    x = mean_acidity,
    y = mean_bitterness,
    size = n_prefer,
    color = coffee
  )
) +
  geom_point(alpha = 0.8)+
  scale_size(
    name = "Number of respondents\npreferring this coffee",
    range = c(4, 14)
  ) +
  scale_color_manual(
    name = "Coffee",
    values = c(
      "Coffee A" = "#6F4E37",  # classic coffee brown
      "Coffee B" = "#8B5A2B",  # lighter roast
      "Coffee C" = "#4B2E2A",  # dark roast
      "Coffee D" = "#A67C52"   # latte brown
    )
  )
+
  labs(
    x = "Mean perceived acidity",
    y = "Mean perceived bitterness",
    title = "Coffee flavor space (size = popularity)"
  ) +
  theme_minimal()



#################
faa_birds <-read_csv("data/wildlife_impacts.csv")


head(faa_birds) 
names(faa_birds)
str(faa_birds)

birds_plot <- ggplot(faa_birds, aes(x = airport,
                                    y = num_engs)) +
  geom_point()

birds_plot 

summarise(faa_birds, )

ggplot(faa_birds, aes(x = ))


faa_birds %>% 
  group_by(operator) %>% 
  summarise(number_per_op = sum(operator))

library(dplyr)

strikes_by_operator <- faa_birds %>%
  count(operator, name = "n_strikes") %>%
  arrange(desc(n_strikes))

ggplot(strikes_by_operator,
       aes(x = operator,
           y = num_engs)) +
  geom_bar()



