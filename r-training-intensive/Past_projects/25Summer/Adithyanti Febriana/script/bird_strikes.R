library(dplyr)
birds_strikes <- read.csv("data/birds_strikes.csv")

range(birds_strikes$date)

summary(birds_strikes)

birds_strikes <- na.omit(birds_strikes)

library(lubridate)
birds_strikes <- birds_strikes %>%
  mutate(date = as.Date(date))

# Visualisation of correlation between time of day and birds strikes occurance from 1990-1999

library(ggplot2)
ggplot(data = birds_strikes)
static_plot <- ggplot(data = birds_strikes,
       mapping = aes(x = date,
                     y = time_of_day,
                     colour = phase_of_flt)) +
  geom_count() +
  scale_x_date(date_breaks = "1 years", date_labels = "%Y") +
  labs(title = "The Birds Strikes Back",
       y = "Time of Day", 
       x = "Year")

library(plotly)
ggplotly(static_plot)

# Visualisation of birds strikes trend from 1990-1999
birds_strikes <- birds_strikes |>
  mutate(birds_seen = if_else(birds_seen == "2-Oct",
                              "2-10",
                              birds_seen))

birds_strikes <- birds_strikes |>
  mutate(birds_struck = if_else(birds_struck == "2-Oct",
                              "2-10",
                              birds_struck))

birds_strikes$birds_struck <- factor(birds_strikes$birds_struck, levels = c("1", "2-10", "11-100" ))

static_birds_plot <- ggplot(data = birds_strikes,
       mapping = aes(x = date,
                     y = height,
                     colour = birds_struck)) +
  geom_count() +
  scale_x_date(date_breaks = "1 years", date_labels = "%Y") +
  labs(title = "Where did the birds struk?",
       y = "Height (m)", 
       x = "Year")

library(plotly)
ggplotly(static_birds_plot)

# Visualisation of birds strikes impacts on flights from 1990-1999
static_severity_plot <- ggplot(data = birds_strikes,
       mapping = aes(x = date,
                     y = effect,
                     colour = phase_of_flt)) +
  geom_count() +
  scale_x_date(date_breaks = "1 years", date_labels = "%Y") +
  labs(title = "How Bad It Was?",
       y = "Effect", 
       x = "Year")

library(plotly)
ggplotly(static_severity_plot)

# Getting statistics for birds strikes dataset
birds_strikes %>% 
  group_by(height) %>% 
  summarise(mean_height = mean(height))


