export default function DatasetsPage() {
    return (
      <main className="min-h-screen bg-gray-50 py-10 px-4">
        <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-2xl p-8">
          <h1 className="text-2xl font-bold text-[#4A6EA9] mb-6">Datasets & Resources</h1>

          <ul className="list-disc pl-6 space-y-3 text-gray-800">
            <li>
              <a
                href="https://encode.su/threads/2105-DNA-Corpus"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline hover:text-blue-800 transition-colors"
              >
                DNA Corpus 1
              </a>
            </li>
            <li>
              <a
                href="https://encode.su/threads/2105-DNA-Corpus"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline hover:text-blue-800 transition-colors"
              >
                DNA Corpus 2
              </a>
            </li>
          </ul>

          {/* <p className="mt-6 text-gray-800">
            Details about the datasets are available <a href="https://encode.su/threads/2105-DNA-Corpus" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline hover:text-blue-800 transition-colors">here</a>.
          </p> */}
        </div>
      </main>
    );
}
