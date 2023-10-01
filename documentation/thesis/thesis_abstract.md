Especially in the construction of low-field MRI devices based on permanent magnets, a large number of magnets are used.
In order to realize a homogeneous B0 field with these magnets, which is necessary for many setups, the magnetic properties of these magnets should be as similar as possible.

Due to the complex manufacturing process, especially of neodymium magnets, the different properties, especially the direction of magnetization, can deviate from each other, which affects the homogeneity of the field.

To adjust the field afterwards, a passive shimming process is typically performed, which is complex and time-consuming and requires manual corrections to the magnets used.

To avoid this process, magnets can be systematically measured in advance. However, in this methodology, the recording, data storage and subsequent evaluation of the data play an important role.

The various existing solutions implement individual aspects, but do not provide a data pipeline from aqusation to analysis.

For this use case, the MagneticReadoutProcessing library was created, which implements different aspects of data acquisition, data storage, analysis, and each intermediate step can be customized by the user without having to create everything from scratch, favoring an exchange between different user groups.