# fuse-test-data-gen
Repository for the Galatea internal data generator tool, used for generating domain data for POCs

This is a complete refactor of the develop branch as of Jan 3rd 2020. It has been rewritten from the ground up to demonstrate a lightweight POC of the generator pattern. This ensures that RAM use is optimised allowing for many millions of records to be egenrated - the current implementation on Develop stored generated records in batches in RAM before writing to file and throws memory errors when writing up to a million records hence this refactor. This is to be used as a guide to refactoring the existing version.
This is very different to the existing version as the multiprocessing and record creation logic has been completely changed.
