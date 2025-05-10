'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Home, Info, bird_sounds, Map, SmartToy, ChatBubbleOutline } from '@mui/icons-material';
import styles from './Header.module.css';


const navItems = [
    { name: 'Home', path: '/', sectionId: '', icon: <Home fontSize="small" /> },
    { name: 'About', path: '/', sectionId: 'about', icon: <Info fontSize="small" /> },
    { name: 'Bird Sounds Explorer', path: '/bird_sounds', sectionId: 'bird_sounds', icon: <bird_sounds fontSize="small" /> },
    { name: 'Interactive Maps', path: '/bird_maps', sectionId: 'bird_maps', icon: <Map fontSize="small" /> },
    { name: 'Bird Assistant', path: '/chat', sectionId: '', icon: <SmartToy fontSize="small" /> }
];

export default function Header() {
    const pathname = usePathname();
    const router = useRouter();
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);


    useEffect(() => {
        if (window) {
            const handleScroll = () => {
                setIsScrolled(window.scrollY > 50)
            }

            window.addEventListener('scroll', handleScroll)
            return () => window.removeEventListener('scroll', handleScroll)
        }

    }, []);
    useEffect(() => {
        if (window) {
            if (pathname === '/' && window.location.hash) {
                const element = document.getElementById(window.location.hash.slice(1));
                if (element) {
                    setTimeout(() => {
                        element.scrollIntoView({ behavior: 'smooth' });
                    }, 100);
                }
            }
        }
    }, [pathname]);

    // Handlers
    function buildHref(item) {

        let href = item.path;
        if ((pathname === "/") && (item.sectionId != '')) {
            href = `#${item.sectionId}`;
        } else {
            if ((item.path === "/") && (item.sectionId != '')) {
                href = item.path + `#${item.sectionId}`;
            } else {
                href = item.path;
            }
        }

        return href;
    }

    return (
        <header
            className={`fixed w-full top-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-black/90' : 'bg-transparent'
                }`}
        >
            <div className="container mx-auto px-4 h-20 flex items-center justify-between">
                <Link href="/" className="text-white hover:text-white/90 transition-colors">
                    <h1 className="text-sm font-bold font-montserrat">🦜Bird Watching App</h1>
                </Link>

                {/* Desktop Navigation */}
                {/* <nav className="hidden md:flex gap-8">
                    <Link href="/" className="text-white hover:text-white/90 transition-colors">
                        Home
                    </Link>
                    <Link href="#about" className="text-white hover:text-white/90 transition-colors">
                        About
                    </Link>
                    <Link href="#bird_sounds" className="text-white hover:text-white/90 transition-colors">
                        bird_sounds
                    </Link>
                    <Link href="#bird_maps" className="text-white hover:text-white/90 transition-colors">
                        bird_maps
                    </Link>
                </nav> */}


                <div className={styles.navLinks}>
                    {navItems.map((item) => (
                        <Link
                            key={item.name}
                            href={buildHref(item)}
                            className={`${styles.navLink} ${pathname === item.path ? styles.active : ''}`}
                        >
                            <span className={styles.icon}>{item.icon}</span>
                            <span className={styles.linkText}>{item.name}</span>
                        </Link>
                    ))}
                </div>

                {/* Mobile Menu Button */}
                <button
                    className="md:hidden p-2"
                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    aria-label="Toggle mobile menu"
                >
                    <div className={`w-6 h-0.5 bg-white mb-1.5 transition-all ${isMobileMenuOpen ? 'rotate-45 translate-y-2' : ''}`} />
                    <div className={`w-6 h-0.5 bg-white mb-1.5 ${isMobileMenuOpen ? 'opacity-0' : ''}`} />
                    <div className={`w-6 h-0.5 bg-white transition-all ${isMobileMenuOpen ? '-rotate-45 -translate-y-2' : ''}`} />
                </button>

                {/* Mobile Menu */}
                <div
                    className={`
                        fixed md:hidden top-20 left-0 w-full bg-white shadow-lg transform transition-transform duration-300
                        ${isMobileMenuOpen ? 'translate-y-0' : '-translate-y-full'}
                    `}
                >
                    <nav className="flex flex-col p-4">
                        <Link
                            href="/"
                            className="py-3 text-gray-800 border-b border-gray-200"
                            onClick={() => setIsMobileMenuOpen(false)}
                        >
                            Home
                        </Link>
                        <Link
                            href="#about"
                            className="py-3 text-gray-800 border-b border-gray-200"
                            onClick={() => setIsMobileMenuOpen(false)}
                        >
                            About
                        </Link>
                        <Link
                            href="#bird_sounds"
                            className="py-3 text-gray-800"
                            onClick={() => setIsMobileMenuOpen(false)}
                        >
                            bird_sounds
                        </Link>
                    </nav>
                </div>
            </div>
        </header>
    )
}