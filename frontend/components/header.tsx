'use client';

import Link from 'next/link';


export function Header() {
  const links = [
    {name: 'About', path: '/about'},
    { name: 'Algorithms', path: '/algo' },
    { name: 'Datasets', path: '/datasets' },
    { name: 'Compressors', path: '/compressor' },
    { name: 'Commands', path: '/commands' },
    { name: 'Links', path: '/links' }
  ]

  return (
    <header className="bg-white border-b">
      <nav className="container mx-auto px-4">
        <ul className="flex justify-center space-x-6 py-4">
          {links.map((link) => (
            <li key={link.name}>
              <Link
                href={link.path}
                className="text-[#4A6EA9] hover:text-[#2C4B82] transition-colors"
              >
                {link.name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  )
}

