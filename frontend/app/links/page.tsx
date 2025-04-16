export default function LinksPage() {
    const compressionLinks = [
      { name: "7-zip", url: "https://www.7-zip.org" },
      { name: "paq8", url: "https://github.com/hxim/paq8px" },
      { name: "bsc", url: "https://github.com/IlyaGrebnov/libbsc" },
      { name: "gzip", url: "https://www.gnu.org/software/gzip/" },
      { name: "zstd", url: "https://github.com/facebook/zstd.git" },
      { name: "bzip2", url: "http://sourceware.org/bzip2" },
      { name: "zpaq", url: "http://mattmahoney.net/dc/zpaq.html" },
      { name: "cmix", url: "https://github.com/byronknoll/cmix" }
    ];
  
    return (
      <main className="min-h-screen bg-gray-50 py-10 px-4">
        <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-2xl p-8">
          <h1 className="text-2xl font-bold text-[#4A6EA9] mb-6">Compression Tools & Resources</h1>
  
          <ul className="list-disc pl-6 space-y-3 text-gray-800">
            {compressionLinks.map((link) => (
              <li key={link.name}>
                <a
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline hover:text-blue-800 transition-colors"
                >
                  {link.name}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </main>
    );
  }
  