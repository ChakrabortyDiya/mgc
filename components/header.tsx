export function Header() {
  const links = [
    "About",
    "Algorithms",
    "Datasets",
    "Compressors",
    "Commands",
    "Links"
  ]

  return (
    <header className="bg-white border-b">
      <nav className="container mx-auto px-4">
        <ul className="flex justify-center space-x-6 py-4">
          {links.map((link) => (
            <li key={link}>
              <a 
                href="#" 
                className="text-[#4A6EA9] hover:text-[#2C4B82] transition-colors"
              >
                {link}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  )
}

