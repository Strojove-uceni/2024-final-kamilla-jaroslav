Machine Learning for Correcting Simulation Outputs in Alpha Particle Measurements with Hybrid Semiconductor Detectors

Authors
Jaroslav Drobný, Kamilla Sabirzyanova

Abstract
Accurately modeling alpha particle interactions in hybrid semiconductor detectors presents a significant challenge. While tools like Geant4 and Allpix Squared effectively simulate energy deposition, they often fail to capture subsequent charge transport and the detector’s full electronic response. As a result, simulated data may lack characteristic features—such as the “halo” effect in alpha particle measurements—leading to discrepancies when compared to real experiments.

This project addresses these shortcomings by employing a CycleGAN-based machine learning approach to transform imperfect simulation outputs into data that closely resemble actual experimental measurements. Using alpha particle data from an Am source recorded on a Timepix 3 ASIC chip with a 500 μm silicon sensor, our method bridges the gap between simulated and experimental data. The resulting synthetic experimental datasets can help researchers better understand complex charge propagation processes and improve future simulation accuracy.

Methodology
We use a CycleGAN model to learn mappings between two domains: simulated and experimental alpha particle measurement data. The CycleGAN framework enables us to correct structural and intensity discrepancies in the simulated images without explicit paired training data. Key steps include:

Data Acquisition and Preparation:
Experimental datasets are collected under conditions identical to those of the simulation. We preprocess and normalize both simulated and experimental images for input into the machine learning model.

Model Selection (CycleGAN):
We chose a CycleGAN due to its ability to perform unpaired image-to-image translation. Unlike supervised models, CycleGAN does not require perfectly matched training pairs, making it ideal for bridging the gap between simulation outputs and experimental results.

Training and Optimization:
The model is trained to preserve structural content while adjusting image characteristics to resemble the experimental distribution. We tune hyperparameters such as the cycle-consistency weight and use validation sets to prevent overfitting.


Code & Results
All code is provided in the accompanying repository. Key components include:

Data Loading and Preprocessing: Scripts to normalize, resize, and partition the datasets into training, validation, and test sets.
Model Definition and Training: Well-commented Python code, highlighting the CycleGAN architecture and training loop, is included in the Jupyter/Colab notebook. Commented code snippets explain the purpose of each function and module.
Evaluation and Visualization:
Generated images are displayed alongside their original simulation inputs and reference experimental data.
We provide figures that compare the structure of clusters before and after CycleGAN transformation, showcasing improvements in the appearance of important features like the “halo” effect.
Quantitative metrics (e.g., SSIM, LPIPS) or domain-specific measures can be included as tables or plots, demonstrating that the generated images are more closely aligned with real experimental patterns.


Conclusions
By integrating a CycleGAN model into the simulation workflow, we successfully reduced discrepancies between simulated and experimental alpha particle measurement data. The results suggest that machine learning-driven post-processing can:

Improve the realism and utility of simulation outputs.
Provide a scalable solution for generating large volumes of synthetic experimental data.
Help researchers gain deeper insights into the behavior of hybrid semiconductor detectors, ultimately aiding in better detector design and calibration.
Although promising, this approach may require further refinement. For instance, spatial misalignments or subtle electronic noise effects may still challenge our model. Future work could involve enhanced preprocessing, domain adaptation techniques, or more advanced neural architectures to refine the results.

