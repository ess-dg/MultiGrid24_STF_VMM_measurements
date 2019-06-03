

# =============================================================================
# Filter
# =============================================================================

def filter_events(events, window):
    # Declare parameters
    parameters = {'adc': [window.ADC_min.value(),
                          window.ADC_max.value(),
                          window.ADC_filter.isChecked()],
                  'channel': [window.channel_min.value(),
                              window.channel_max.value(),
                              window.channel_filter.isChecked()],
                  'srs_timestamp': [float(window.time_min.text()),
                                    float(window.time_max.text()),
                                    window.timestamp_filter.isChecked()],
                  'chip_id': [window.chip_min.value(),
                              window.chip_max.value(),
                              window.chip_filter.isChecked()],
                  }
    # Only include the filters that we want to use
    events_red = events
    for par, (min_val, max_val, filter_on) in parameters.items():
        if filter_on:
            events_red = events_red[(events_red[par] >= min_val)
                                    & (events_red[par] <= max_val)]
    return events_red
















