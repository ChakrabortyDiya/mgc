import { Header } from "../components/header"
import { WelcomeBox } from "../components/welcome-box"
import { QuickSelector } from "../components/quick-selector"
// import { CustomComparison } from "../components/custom-comparison"
// import { CompressorSelector } from "../components/compressor-selector"
// import { OutputConfiguration } from "../components/output-configuration"
import ComparisonPage from "../components/ComparisonPage"


export default function Page() {
  return (
    
      <div className="min-h-screen bg-white">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-semibold text-[#4A6EA9] text-center mb-8">NGC: Normalised Genome Compressors</h1>
          <WelcomeBox />
          <QuickSelector />
          <div className="space-y-8">
            <ComparisonPage />
            {/* <CompressorSelector />
            <OutputConfiguration selectedGenomes={[]} /> */}
          </div>
          <footer className="text-center text-sm text-gray-600 pt-8">
          By <a href="#" className="text-blue-600 hover:underline">Contributors</a>, 2023-2026, public domain
        </footer>
        </main>
      </div>
    
  )
}

