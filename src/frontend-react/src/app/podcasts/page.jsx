'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import PodcastCard from '@/components/shared/PodcastCard';
//import DataService from "../../services/MockDataService"; // Mock
import DataService from "../../services/DataService";

// Import the styles
import styles from "./styles.module.css";

export default function PodcastsPage() {
    // Component States
    const [episodes, setEpisodes] = useState([]);

    // Setup Component
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await DataService.GetPodcasts(100);
                setEpisodes(response.data);
            } catch (error) {
                console.error('Error fetching podcasts:', error);
                setEpisodes([]); // Set empty array in case of error
            }
        };

        fetchData();
    }, []);

    return (
        <div className={styles.container}>
            {/* Hero Section */}
            <section className={styles.hero}>
                <div className={styles.heroContent}>
                    <h1>Bird Sounds Explorer</h1>
                    <p>Explore the rich diversity of birdlife through their calls.</p>
                </div>
            </section>

            {/* About Section */}
            <section className={styles.about}>
                <div className={styles.aboutContent}>
                    <h2>About Bird Sounds Explorer</h2>
                    <p>
                    Welcome to our bird sounds collection! This unique library features the vocalizations of bird species from Yanachaga Chemillén National Park.
                    Each recording offers a window into the natural world—an invitation to explore the rich diversity of birdlife through their calls.
                    Whether you are a curious listener or a dedicated birdwatcher, our collection lets you experience the forest in a whole new way.
                    </p>
                </div>
            </section>

            <div className={styles.episodesList}>
                {episodes.map((episode) => (
                    <PodcastCard key={episode.id} podcast={episode}></PodcastCard>
                ))}
            </div>


        </div>
    )
}

