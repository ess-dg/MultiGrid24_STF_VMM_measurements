import numpy as np

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
    # Perform an additional filter on grid and wire channels
    wCh_filter_on = window.wCh_filter.isChecked()
    wCh_min = window.wCh_min.value()
    wCh_max = window.wCh_max.value()
    gCh_filter_on = window.gCh_filter.isChecked()
    gCh_min = window.gCh_min.value()
    gCh_max = window.gCh_max.value()

    if wCh_filter_on and gCh_filter_on:
        events_red = events_red[((events_red['wCh'] >= wCh_min)
                                 & (events_red['wCh'] <= wCh_max)) |
                                ((events_red['gCh'] >= gCh_min)
                                 & (events_red['gCh'] <= gCh_max))]
    elif wCh_filter_on and (not gCh_filter_on):
        events_red = events_red[((events_red['wCh'] >= wCh_min)
                                 & (events_red['wCh'] <= wCh_max)) |
                                ((events_red['gCh'] >= 0)
                                 & (events_red['gCh'] <= 12))]
    elif (not wCh_filter_on) and gCh_filter_on:
        events_red = events_red[((events_red['wCh'] >= 0)
                                 & (events_red['wCh'] <= 79)) |
                                ((events_red['gCh'] >= gCh_min)
                                 & (events_red['gCh'] <= gCh_max))]
    print(events_red)
    return events_red


def filter_coincident_events(ce, window):
    # Declare parameters
    parameters = {'Time': [float(window.time_min.text()),
                           float(window.time_max.text()),
                           window.timestamp_filter.isChecked()],
                  'wADC': [float(window.wADC_min.text()),
                           float(window.wADC_max.text()),
                           window.wADC_filter.isChecked()],
                  'gADC': [float(window.gADC_min.text()),
                           float(window.gADC_max.text()),
                           window.gADC_filter.isChecked()],
                  'wM': [window.wM_min.value(),
                         window.wM_max.value(),
                         window.wM_filter.isChecked()],
                  'gM': [window.gM_min.value(),
                         window.gM_max.value(),
                         window.gM_filter.isChecked()]
                  }
    # Only include the filters that we want to use
    ce_red = ce
    for par, (min_val, max_val, filter_on) in parameters.items():
        if filter_on:
            ce_red = ce_red[(ce_red[par] >= min_val)
                            & (ce_red[par] <= max_val)]
    # Perform an additional filter on grid and wire channels
    wCh_filter_on = window.wCh_filter.isChecked()
    wCh_min = window.wCh_min.value()
    wCh_max = window.wCh_max.value()
    gCh_filter_on = window.gCh_filter.isChecked()
    gCh_min = window.gCh_min.value()
    gCh_max = window.gCh_max.value()
    
    if wCh_filter_on and gCh_filter_on:
        ce_red = ce_red[((ce_red['wCh'] >= wCh_min) & (ce_red['wCh'] <= wCh_max)) |
                        ((ce_red['gCh'] >= gCh_min) & (ce_red['gCh'] <= gCh_max))]
    elif wCh_filter_on and (not gCh_filter_on):
        ce_red = ce_red[((ce_red['wCh'] >= wCh_min) & (ce_red['wCh'] <= wCh_max)) |
                        ((ce_red['gCh'] >= 0) & (ce_red['gCh'] <= 12))]
    elif (not wCh_filter_on) and gCh_filter_on:
        ce_red = ce_red[((ce_red['wCh'] >= 0) & (ce_red['wCh'] <= 79)) |
                        ((ce_red['gCh'] >= gCh_min) & (ce_red['gCh'] <= gCh_max))]
    return ce_red
