                        For the culmination of my Bachelors Degree for Electrical And Computer Engeering, I Worked with three other students to plan, design, and create a
                        Capstone Design Project that employed skills I have learned throughout my 5 years at The Ohio State University. After much deliberation, my team
                        decided to address issues surrounding Marathon Gas Companies current process involving calibrating their gas sensors.
                        The issue stems from the exposure to Harmful H2S (Hydrogen Sulphide) gas that Marathon employees face working within the field. The gas sensors they
                        use to detect H2S gas need to be calibrated every 30 days to ensure they remain functional. Maraton's calibration process includes placing their sensors
                        onto the calibration bench, which would then release small amounts of H2S gas into the air without any protection for the employee.
                        
                        Because of this, my team and I designed a containment chamber that would house the calibration bench, and contain the H2S Released. During the design phase,
                        our team designated 4 major subsystems for the project: The Chamber Itself, The Control System, The Disposal System, and the Human Machine Interface. I was
                        responsible for the Human Machine Interface, which would allow the user to interact with the system, and monitor the calibration process. Unfortunately, due to
                        university restrictions on funding and gas acquisition, we were unable to fully implement the Disposal/Control System, and H2S was too dangerous to use. H2 gas
                        was instead used as a substitute to demonstrate a proof of concept.

                        For the Human Machine Interface, I decided to utilize a Python, PyQt6, and a Raspberry Pi 4. Our team purchased a 7 inch touch screen display, aswell as a POSIFA
                        HGS1004 Hydrogen Sensor which connected to the GPIO Pins on the raspberry pi. The Sensor utilized I2C Communication protocol and was used to communicate with the
                        python script in order to implement a live graph of H2 Gas levels within the chamber, and determine when the calibration process was complete. The interface also
                        included an event log, that tracks each calibration process, and writes important information about each calibration to a text file. This text file is also used
                        to recreate the live graph of H2 Gas levels, and display it to the user, along with any warnings generated throughout the process.
