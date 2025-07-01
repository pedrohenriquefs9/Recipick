export function RecipeCard({ title, content, imageURL, onClick }) {
  return (
    <button
      onClick={onClick}
      className="bg-solid shadow-md rounded-2xl p-4 flex flex-col items-center justify-center gap-2 w-full cursor-pointer hover:shadow-lg transition-shadow duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
    >
      <img
        src={imageURL}
        alt={title}
        className="w-full h-48 object-cover rounded-md mb-4 bg-solid-dark flex items-center justify-center"
      />
      <h2 className="w-full text-start">{title}</h2>
    </button>
  );
}
