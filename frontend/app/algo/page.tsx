// pages/algo.tsx

export default function AlgoPage() {
    return (
      <main className="min-h-screen bg-gray-50 py-10 px-4">
        <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-2xl p-8">
          <h1 className="text-2xl font-bold text-[#4A6EA9] mb-6">The steps of the NGC algorithm</h1>
          
          <div className="space-y-4 text-gray-800 leading-relaxed">
            <p><strong>Input:</strong> A DNA or RNA sequence</p>
  
            <ol className="list-decimal list-inside space-y-2">
              <li>Convert FASTA, multi-FASTA or FASTQ sequence to raw data consisting only of <code>{`{A, C, G, T/U, etc}`}</code></li>
              <li>Convert lower-case <code>{`{a, c, g, t/u}`}</code> to upper-case <code>{`{A, C, G, T/U}`}</code></li>
              <li>Remove all other IUPAC characters (e.g. <code>N</code>, <code>K</code>, <code>B</code>, etc.)</li>
              <li>Convert the cleaned sequence into 2-bit encoding (stores 4 nucleotides per byte, e.g., <code>ACGTT → 01233</code>)</li>
              <li>Convert every 4 two-bit-coded nucleotides into extended ASCII code</li>
              <li>Apply general-purpose encoder</li>
            </ol>
  
            <p><strong>Output:</strong> Compressed sequence</p>
          </div>
        </div>
      </main>
    );
  }
  
 

