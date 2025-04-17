
'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import styles from './Podcasts.module.css';
import PodcastCard from '../shared/PodcastCard';
//import DataService from "../../services/MockDataService"; // Mock
import DataService from "../../services/DataService";


export default function Podcasts() {
    // Component States
    const [episodes, setEpisodes] = useState([]);

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.GetPodcasts(4); // Limiting to 4 episodes for the main view
                setEpisodes(response.data);
            } catch (error) {
                console.error('Error fetching podcasts:', error);
                setEpisodes([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);

    return (
        <section className={styles.section} id="podcasts">
            <h2 className={styles.title}>Bird Sounds Explorer</h2>
            <div className={styles.underline}></div>

            <div className={styles.content}>
                <div className={styles.aboutPodcast} style={{ marginTop: '40px' }}>

                    <h3>About Bird Sounds Explorer</h3>
                    <p>
                        Welcome to the Bird Sounds Explorer, where we celebrate the incredible diversity of birds 
                        through their unique calls! 
                    </p>
                    <p>                        
                        Each bird call offers a glimpse into the vibrant ecosystems 
                        of the Yanachaga Chemillén National Park. 
                    </p> 
                    <p>   
                        Join us as we explore the natural symphony of the forest—one bird at a time.
                    </p>
                </div>

                <div className={styles.episodesList}>
                    {episodes[3] && (
                        <PodcastCard key={episodes[3].id} podcast={episodes[3]} />
                    )}
                </div>

            </div>
            <div className={styles.viewAllContainer}>
                <Link href="/podcasts" className={styles.viewAllButton}>
                    Access Bird Sounds Explorer
                </Link>
            </div>
        </section>
    )
}