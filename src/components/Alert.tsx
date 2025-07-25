type AlertProps = {
  errorMessage: string | null;
  className?: React.HTMLAttributes<unknown>["className"];
};

export const Alert = ({ errorMessage, className }: AlertProps) => {
  return (
    <div
      role="alert"
      className={`alert alert-error alert-soft ${
        errorMessage ? "opacity-100" : "opacity-0 -translate-y-full"
      } transition-all duration-300 ${className}`}
    >
      <span>{errorMessage}</span>
    </div>
  );
};
