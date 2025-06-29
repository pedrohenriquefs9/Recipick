import ReactMarkdown from 'react-markdown';

export function AIMessage({ message }) {
  return (
    <div className="flex flex-col prose prose-sm items-start justify-start p-4 bg-solid text-black rounded-xl shadow-md text-sm max-w-full leading-relaxed">
      <ReactMarkdown
        components={{
          hr: () => <hr className="border-t-1 border-dark-light my-4 w-full" />
        }}
      >
        {message}
      </ReactMarkdown>
    </div>
  );
}
