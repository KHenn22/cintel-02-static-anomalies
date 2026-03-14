# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
Static data from a pediatric (children's) clinic's patient records.  There are two columns, age_years & height_inches.  The clinic serves patients up until the age of 16.

### Signals
Used:
age_years: the patient age in years
height_inches: The patient height in inches

Created:
severity_level: overall worst severity between age and height
age_severity: how far the age exceeds the valid range (16)
height_severity: how far the height exceeds the valid range (72")

### Experiments
I added severity classification to the anomaly detection pipeline.  Tested different thresholds.  Because of the high ages above the threshold, nearly any reasonable option would be a severe anamoly.  Considered a wider age range but opted to keep it tighter.

### Results
24 anomalies detected.  23 were flagged severe due to age with one being flagged moderate.  One height was flagged mild, but due to the age being severe (49) was classified overall severe.

### Interpretation
The data suggests that this dataset is invalid for a children's clinic or that there are serious QC gaps with inputted data.  Likely a comprehensive quality review of records would need to be undertaken as these issues may be indicative of larger issues.
