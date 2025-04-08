import { Header } from "../components/header"
import { WelcomeBox } from "../components/welcome-box"
import { QuickSelector } from "../components/quick-selector"
import { CustomComparison } from "../components/custom-comparison"
import { CompressorSelector } from "../components/compressor-selector"
import { OutputConfiguration } from "../components/output-configuration"

export default function Page() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-semibold text-[#4A6EA9] text-center mb-8">NGC: Normalised Genome Compressors</h1>
        <WelcomeBox />
        <QuickSelector />
        <div className="space-y-8">
          <CustomComparison />
          <CompressorSelector />
          <OutputConfiguration />
        </div>
      </main>
    </div>
  )
}

